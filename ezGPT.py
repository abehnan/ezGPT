#!/usr/bin/python3

import json
import os
import requests
import sys

MODEL = "gpt-3.5-turbo"
NUM_EMPTY_LINES_TO_SEND_REQUEST = 3
SYSTEM_MESSAGE = "You are a helpful assistant."
TEMPERATURE = 1


def get_user_input():
    print()
    print("---")
    print("## User")
    print("---")
    user_input = ""
    empty_count = 0

    while True:
        line = input()

        if line == "":
            empty_count += 1
        else:
            empty_count = 0

        if empty_count >= NUM_EMPTY_LINES_TO_SEND_REQUEST:
            break

        user_input += line + "\n"

    return user_input


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
    print(message["content"])


def respond():
    print("---")
    print("## AI")
    print("---")
    response = send_request()
    consume_response(response)


if __name__ == "__main__":
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]

    if len(sys.argv) > 1:
        conversation.append({"role": "user", "content": ' '.join(sys.argv[1:])})
        respond()

    while True:
        conversation.append({"role": "user", "content": get_user_input()})
        respond()
