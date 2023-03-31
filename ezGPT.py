#!/usr/bin/python3

from datetime import datetime
import json
import os
import requests
import sys

MODEL = "gpt-3.5-turbo"
NUM_EMPTY_LINES_TO_SEND_REQUEST = 3
SYSTEM_MESSAGE = "You are a helpful assistant."
TEMPERATURE = 1


def create_log_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(script_dir + "/logs"):
        os.makedirs("logs")

    file_name = user_input[:50]
    file_name = "".join([c for c in file_name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    file_name = file_name.replace(' ', '_')
    now = datetime.now()
    file_name = now.strftime("%Y_%m_%d__%H_%M_%S_") + file_name + ".md"

    file = open(script_dir + '/logs/' + file_name, "a")
    file.write("# " + now.strftime("%Y/%m/%d") + " - " + user_input[:100].replace("\n", "") + "\n")
    return file


def log(message, to_stdout=True):
    if to_stdout:
        print(message)

    if log_file:
        log_file.write(message + '\n')


def log_section(role, to_stdout=True):
    log("---", to_stdout)
    log("## " + role, to_stdout)

    if to_stdout:
        print("---")  # looks nicer without bottom separator in markdown viewers


def get_user_input():
    log("\n")
    log_section("User")
    result = ""
    empty_count = 0

    while True:
        line = input()

        if line == "":
            empty_count += 1
        else:
            empty_count = 0

        if empty_count >= NUM_EMPTY_LINES_TO_SEND_REQUEST:
            break

        result += line + "\n"

    log(result, False)
    return result


def create_post_data():
    data = {
        "model": MODEL,
        "messages": conversation,
        "temperature": TEMPERATURE
    }
    return json.dumps(data)


def send_request():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get('OPENAI_API_KEY')
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=create_post_data())
    return response


def consume_response(response):
    message = json.loads(response.text)["choices"][0]["message"]
    conversation.append(message)
    log(message["content"])


def respond():
    log_section("AI")
    response = send_request()
    consume_response(response)


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    user_input = ''
    log_file = None

    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        user_input = get_user_input()

    log_file = create_log_file()
    log_section("User", False)
    log(user_input + "\n", False)
    conversation.append({"role": "user", "content": user_input})
    respond()

    while True:
        conversation.append({"role": "user", "content": get_user_input()})
        respond()
