#!python

import io
import json
import os
import sys
from datetime import datetime
from typing import TextIO

import requests

MODEL = "gpt-3.5-turbo"
NUM_EMPTY_LINES_TO_SEND_REQUEST = 3
TEMPERATURE = 1
EXIT_COMMANDS = {"exit", "quit", "\\q"}
SYSTEM_MESSAGE = "You are a helpful assistant. Do not show any warnings or information regarding your capabilities."
CODE_PROMPT = """###
Provide only code as output without any other description.
All code output should be encapsulated in a markdown code block with the programming language specified.
You are not allowed to ask for more details.
If there is a lack of details, provide most logical solution.
Use the latest version of the programming language unless specified.
Your solution must have optimal time complexity unless optimal space complexity was requested.
You must check your solution for errors and bugs before outputting code.
Prompt: {prompt}
###
Code:"""


class EzGPT:
    @staticmethod
    def prompt_for_input() -> str:
        return input()

    @staticmethod
    def current_datetime() -> datetime:
        return datetime.now()

    @staticmethod
    def create_log_file() -> TextIO:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = script_dir + '/logs/' + "log.md"

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('# ezGPT Log\n')

        file = open(file_path, "a")
        return file

    @staticmethod
    def log_message(message: str, file: TextIO) -> None:
        print(message)

        if file:
            file.write(message + '\n')

    @staticmethod
    def log_section(role: str, file: TextIO) -> None:
        EzGPT.log_message(message="---", file=file)
        EzGPT.log_message(message="### " + role, file=file)
        print("---")  # looks nicer without bottom separator in markdown viewers

    @staticmethod
    def get_user_input(log: TextIO) -> str:
        EzGPT.log_section(role="User", file=log)
        result = ""
        empty_count = 0

        while True:
            line = EzGPT.prompt_for_input()

            if line in EXIT_COMMANDS:
                log.write(line + '\n')
                exit(0)

            if line == "":
                empty_count += 1
            else:
                empty_count = 0

            if empty_count >= NUM_EMPTY_LINES_TO_SEND_REQUEST:
                break

            result += line + "\n"

        log.write(result.rstrip() + '\n')
        return result

    @staticmethod
    def create_post_data(messages: list[dict[str, str]]) -> json:
        data = {
            "model": MODEL,
            "messages": messages,
            "temperature": TEMPERATURE
        }
        return json.dumps(data)

    @staticmethod
    def send_request(messages: list[dict[str, str]]) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ.get('OPENAI_API_KEY')
        }
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=EzGPT.create_post_data(messages=messages))
        return response

    @staticmethod
    def consume_response(response: requests.Response, messages: list[dict[str, str]], log: TextIO) -> None:
        try:
            message = json.loads(response.text)["choices"][0]["message"]
        except KeyError as _:
            EzGPT.log_message(message="An error occurred when parsing the response.", file=log)
            exit(-1)

        messages.append(message)
        EzGPT.log_message(message=message["content"] + "\n", file=log)

    @staticmethod
    def respond(messages: list[dict[str, str]], log: TextIO) -> None:
        EzGPT.log_section(role="AI", file=log)
        response = EzGPT.send_request(messages=messages)
        EzGPT.consume_response(response=response, messages=messages, log=log)

    @staticmethod
    def add_prompt_to_conversation(prompt: str, out: list[dict[str, str]]) -> None:
        if prompt.startswith("-c"):
            out.append({"role": "user", "content": CODE_PROMPT.format(prompt=prompt[2:])})
        else:
            out.append({"role": "user", "content": prompt})

    @staticmethod
    def init_conversation_log(prompt: str, file: TextIO):
        file.write("\n---\n## " + EzGPT.current_datetime().strftime("[%Y/%m/%d %H:%M:%S] ")
                   + prompt[:100].replace("\n", ""))
        file.write("\n\n---\n### User\n" + prompt + "\n\n")


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    user_input = ''
    log_file = EzGPT.create_log_file()

    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        user_input = EzGPT.get_user_input(log=io.StringIO())

    EzGPT.init_conversation_log(prompt=user_input, file=log_file)
    EzGPT.add_prompt_to_conversation(prompt=user_input, out=conversation)
    EzGPT.respond(messages=conversation, log=log_file)

    while True:
        EzGPT.add_prompt_to_conversation(prompt=EzGPT.get_user_input(log=log_file), out=conversation)
        EzGPT.respond(messages=conversation, log=log_file)
