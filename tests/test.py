import io
import os
from datetime import datetime
from unittest.mock import patch

import requests

from ezGPT import EzGPT


class TestEzGPT:
    def test_create_log_file(self):
        log_file = EzGPT.create_log_file()
        assert isinstance(log_file, io.TextIOWrapper)

    def test_log_message(self, capsys):
        log_file = io.StringIO()
        message = "Test message"
        EzGPT.log_message(message=message, file=log_file)
        captured = capsys.readouterr()
        assert captured.out == "Test message\n"
        assert log_file.getvalue() == 'Test message\n'

    def test_log_section(self, capsys):
        log_file = io.StringIO()
        EzGPT.log_section(role="Test", file=log_file)
        captured = capsys.readouterr()
        assert captured.out == "---\n### Test\n---\n"
        assert log_file.getvalue() == "---\n### Test\n"

    def test_create_post_data(self):
        messages = [{"role": "user", "content": "Hi"}, {"role": "AI", "content": "Hello"}]
        post_data = EzGPT.create_post_data(messages=messages)
        expected = (
            '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hi"}, '
            '{"role": "AI", "content": "Hello"}], "temperature": 1}'
        )
        assert post_data == expected

    def test_send_request(self):
        if not os.environ.get('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = 'fake_api_key'

        messages = [{"role": "user", "content": "Hi"}]

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            EzGPT.send_request(messages=messages)

        mock_post.assert_called_once()
        mock_post.assert_called_with(
            url='https://api.openai.com/v1/chat/completions',
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer fake_api_key'},
            data='{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hi"}], "temperature": 1}')

    def test_consume_response(self):
        messages = [{"role": "user", "content": "Hi"}]
        response = requests.Response()
        response._content = '{"choices": [{"message": {"role": "AI", "content": "Hello"}}]}'.encode('utf-8')
        log = io.StringIO()
        EzGPT.consume_response(response=response, messages=messages, log=log)
        assert len(messages) == 2
        assert messages[1]['role'] == 'AI'
        assert messages[1]['content'] == 'Hello'
        assert log.getvalue().strip() == 'Hello'

    def test_respond(self):
        messages = [{"role": "user", "content": "Hi"}]

        with patch('ezGPT.EzGPT.send_request') as mock_send_request:
            mock_send_request.return_value = requests.Response()
            mock_send_request.return_value._content = \
                '{"choices": [{"message": {"role": "AI", "content": "Hello"}}]}'.encode('utf-8')
            log = io.StringIO()
            EzGPT.respond(messages=messages, log=log)

        mock_send_request.assert_called_once()
        assert len(messages) == 2
        assert messages[1]['role'] == 'AI'
        assert messages[1]['content'] == 'Hello'
        assert log.getvalue() == '---\n### AI\nHello\n\n'

    def test_add_prompt_to_conversation(self):
        out = []
        EzGPT.add_prompt_to_conversation(prompt='Test prompt', out=out)
        assert len(out) == 1
        assert out[0]['role'] == 'user'
        assert out[0]['content'] == 'Test prompt'
        out = []
        EzGPT.add_prompt_to_conversation(prompt='-cTest prompt code', out=out)
        assert len(out) == 1
        assert out[0]['role'] == 'user'
        assert out[0]['content'] == \
               '###\nProvide only code as output without any other description.\n' \
               'All code output should be encapsulated in a markdown code block with the ' \
               'programming language specified.\nYou are not allowed to ask for more details.' \
               '\nIf there is a lack of details, provide most logical solution.\nUse the latest version of the ' \
               'programming language unless specified.\nYour solution must have optimal time complexity unless ' \
               'optimal space complexity was requested.\nYou must check your solution for errors and bugs before ' \
               'outputting code.\nPrompt: Test prompt code\n###\nCode:'

    @patch('ezGPT.EzGPT.current_datetime',
           return_value=datetime(year=2023, month=4, day=3, hour=10, minute=38, second=43))
    def test_init_conversation_log(self, _):
        log = io.StringIO()
        user_input = 'Test input'
        EzGPT.init_conversation_log(prompt=user_input, file=log)
        assert log.getvalue() == '\n---\n## [2023/04/03 10:38:43] Test input\n\n---\n### User\nTest input\n\n'

    @patch('ezGPT.EzGPT.prompt_for_input', side_effect=["Test input", "", "", ""])
    def test_get_user_input(self, _):
        log = io.StringIO()
        user_input = EzGPT.get_user_input(log=log)
        assert user_input == "Test input\n\n\n"
        assert log.getvalue() == "---\n### User\nTest input\n"
