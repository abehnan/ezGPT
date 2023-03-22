#!/usr/bin/python3

import json
import os
import requests
import sys

NUM_EMPTY_LINES_TO_SEND_REQUEST = 2
TEMPERATURE = 1


def get_user_input():
    print()
    print("----------------------------------------------------")
    print("                      User")
    print("----------------------------------------------------")
    user_input = ""
    empty_count = 0

    while True:
        line = input()

        if line == "":
            empty_count += 1
        else:
            empty_count = 0

        if empty_count >= NUM_EMPTY_LINES_TO_SEND_REQUEST:
            print("----------------------------------------------------")
            print("               Sending request...")
            print("----------------------------------------------------")
            print()
            break

        user_input += line + "\n"

    return user_input


def create_post_data(conversation):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation,
        "temperature": TEMPERATURE
    }
    return json.dumps(data)


def send_request(conversation):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get('OPENAI_API_KEY')
    }
    data = create_post_data(conversation)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
    return response


def consumeResponse(response):
    content = json.loads(response.text)["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": content})
    print_response(content)


def print_response(content):
    print("----------------------------------------------------")
    print("                     AI")
    print("----------------------------------------------------")
    print(content)


if __name__ == "__main__":
    conversation = [{
        "role": "system",
        "content": "You are a helpful programming assistant. You will minimize prose and verbosity in non-code answers."
    }]
    print("----------------------------------------------------")
    print("                 ezGPT started.")
    print("----------------------------------------------------")

    if len(sys.argv) > 1:
        conversation.append({"role": "user", "content": ' '.join(sys.argv[1:])})
        response = send_request(conversation)
        consumeResponse(response)

    while True:
        conversation.append({"role": "user", "content": get_user_input()})
        response = send_request(conversation)
        consumeResponse(response)

