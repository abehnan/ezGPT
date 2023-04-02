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
Provide only code as output without any description using Markdown formatting.
If there is a lack of details, provide most logical solution.
Use the latest version of the programming language unless specified.
Your solution must have optimal time complexity unless optimal space complexity was requested.
You must check your solution for errors and bugs before responding.
You are not allowed to ask for more details.
Prompt: {prompt}
###
Code:"""


def create_log_file() -> TextIO:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = script_dir + '/logs/' + "log.md"

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('# ezGPT Log\n')

    file = open(file_path, "a")
    return file


def log_message(message: str, file: TextIO) -> None:
    print(message)

    if file:
        file.write(message + '\n')


def log_section(role: str, file: TextIO) -> None:
    log_message(message="---", file=file)
    log_message(message="### " + role, file=file)
    print("---")  # looks nicer without bottom separator in markdown viewers


def get_user_input(log: TextIO) -> str:
    log_section(role="User", file=log)
    result = ""
    empty_count = 0

    while True:
        line = input()

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

    log.write(result + '\n')
    return result


def create_post_data(messages: list[dict[str, str]]) -> json:
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE
    }
    return json.dumps(data)


def send_request(messages: list[dict[str, str]]) -> requests.Response:
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get('OPENAI_API_KEY')
    }
    response = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=create_post_data(messages=messages))
    return response


def consume_response(response: requests.Response, messages: list[dict[str, str]], log: TextIO) -> None:
    try:
        message = json.loads(response.text)["choices"][0]["message"]
    except KeyError as _:
        log_message(message="An error occurred when parsing the response.", file=log)
        exit(-1)

    messages.append(message)
    log_message(message=message["content"] + "\n", file=log)


def respond(messages: list[dict[str, str]], log: TextIO) -> None:
    log_section(role="AI", file=log)
    response = send_request(messages=messages)
    consume_response(response=response, messages=messages, log=log)


def add_prompt_to_conversation(prompt: str, out: list[dict[str, str]]) -> None:
    if prompt.startswith("-c"):
        out.append({"role": "user", "content": CODE_PROMPT.format(prompt=prompt[2:])})
    else:
        out.append({"role": "user", "content": prompt})


def init_conversation_log(file: TextIO):
    file.write("\n## " + datetime.now().strftime("[%Y/%m/%d %H:%M:%S] ") + user_input[:100].replace("\n", ""))
    file.write("\n\n---\n### User\n" + user_input + "\n\n")


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    user_input = ''
    log_file = create_log_file()

    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        user_input = get_user_input(log=io.StringIO())

    init_conversation_log(file=log_file)
    add_prompt_to_conversation(prompt=user_input, out=conversation)
    respond(messages=conversation, log=log_file)

    while True:
        add_prompt_to_conversation(prompt=get_user_input(log=log_file), out=conversation)
        respond(messages=conversation, log=log_file)
