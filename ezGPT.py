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


def create_log_file(first_message: str) -> TextIO:
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(script_dir + "/logs"):
        os.makedirs("logs")

    file_name = first_message[:50]
    file_name = "".join([c for c in file_name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    file_name = file_name.replace(' ', '_')
    now = datetime.now()
    file_name = now.strftime("%Y_%m_%d__%H_%M_%S_") + file_name + ".md"

    file = open(script_dir + '/logs/' + file_name, "a")
    file.write("# " + now.strftime("[%Y/%m/%d] ") + first_message[:100].replace("\n", "") + "\n")
    return file


def log(message: str, to_stdout: bool, file: TextIO) -> None:
    if to_stdout:
        print(message)

    if file:
        file.write(message + '\n')


def log_section(role: str, to_stdout: bool, file: TextIO) -> None:
    log(message="---", to_stdout=to_stdout, file=file)
    log(message="## " + role, to_stdout=to_stdout, file=file)

    if to_stdout:
        print("---")  # looks nicer without bottom separator in markdown viewers


def get_user_input(should_log_section: bool, out_file: TextIO) -> str:
    log(message="\n", to_stdout=should_log_section, file=out_file)
    log_section(role="User", to_stdout=should_log_section, file=out_file)
    result = ""
    empty_count = 0

    while True:
        line = input()

        if line in EXIT_COMMANDS:
            log(message=line, to_stdout=False, file=out_file)
            exit(0)

        if line == "":
            empty_count += 1
        else:
            empty_count = 0

        if empty_count >= NUM_EMPTY_LINES_TO_SEND_REQUEST:
            break

        result += line + "\n"

    log(message=result, to_stdout=False, file=out_file)
    return result


def create_post_data(messages: list[dict[str, str]]) -> json:
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE
    }
    return json.dumps(obj=data)


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


def consume_response(response: requests.Response, out_messages: list[dict[str, str]], out_file: TextIO) -> None:
    try:
        message = json.loads(response.text)["choices"][0]["message"]
    except KeyError as _:
        log(message="An error occurred when parsing the response.", to_stdout=True, file=out_file)
        exit(-1)

    out_messages.append(message)
    log(message=message["content"], to_stdout=True, file=out_file)


def respond(messages: list[dict[str, str]], out_file: TextIO) -> None:
    log_section(role="AI", to_stdout=True, file=out_file)
    response = send_request(messages=messages)
    consume_response(response=response, out_messages=messages, out_file=out_file)


def add_prompt_to_conversation(prompt: str, out: list[dict[str, str]]) -> None:
    if prompt.startswith("-c"):
        out.append({"role": "user", "content": CODE_PROMPT.format(prompt=prompt[2:])})
    else:
        out.append({"role": "user", "content": prompt})


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    user_input = ''
    log_file = None

    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        user_input = get_user_input(should_log_section=True, out_file=io.StringIO())

    log_file = create_log_file(first_message=user_input)
    log_section(role="User", to_stdout=False, file=log_file)
    log(message=user_input + "\n", to_stdout=False, file=log_file)

    add_prompt_to_conversation(prompt=user_input, out=conversation)
    respond(messages=conversation, out_file=log_file)

    while True:
        add_prompt_to_conversation(get_user_input(should_log_section=True, out_file=log_file), out=conversation)
        respond(messages=conversation, out_file=log_file)
