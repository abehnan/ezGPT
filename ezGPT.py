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


def setup_log_file():
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists(script_dir + "/logs"):
        os.makedirs("logs")

    clean_input = user_input[:50]
    clean_input = "".join([c for c in clean_input if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    clean_input = clean_input.replace(' ', '_')

    file_name = datetime.now().strftime("%Y_%m_%d__%H_%M_%S_") + clean_input + ".md"
    file = open(script_dir + '/logs/' + file_name, "a")
    file.write("# " + file_name + "\n")
    return file


def log(message):
    print(message)

    if log_file:
        log_file.write(message + '\n')


def log_user_input_template():
    log("\n")
    log("---")
    log("## User")
    print("---")  # looks nicer without bottom separator in markdown viewers


def get_user_input():
    log_user_input_template()
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
    data = create_post_data()
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
    return response


def consume_response(response):
    message = json.loads(response.text)["choices"][0]["message"]
    conversation.append(message)
    log(message["content"])


def respond():
    log("---")
    log("## AI")
    print("---")  # looks nicer without bottom separator in markdown viewers
    response = send_request()
    consume_response(response)


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    user_input = ''
    log_file = None

    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        log_file = setup_log_file()
    else:
        user_input = get_user_input()
        log_file = setup_log_file()

    log_user_input_template()
    log(user_input + "\n")
    conversation.append({"role": "user", "content": user_input})
    respond()

    while True:
        conversation.append({"role": "user", "content": get_user_input()})
        respond()
