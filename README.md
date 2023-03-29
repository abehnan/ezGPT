# ezGPT
Welcome to the ezGPT GitHub project!

This is a terminal-based chatbot that uses GPT technology to power its conversations.

The purpose of this project is to provide users with a simple and easy-to-use chatbot that can help them in their day-to-day tasks or even just provide some fun conversation.

This project was designed with simplicity in mind and is meant to be easily customizable and extendable. With just a few lines of code, you can alter the chatbot's behavior to fit your specific needs.

## Setup

In `~/.bashrc`:

```
export OPENAI_API_KEY='<YOUR_OPENAI_KEY_HERE>'
alias gpt='python /path/to/cloned/repository/ezGPT.py'
```

## Usage

You can prompt gpt direcly from your terminal by preprending your prompt with `gpt`.

```
[anon:~]$ gpt what is the average lifespan of a chimpanzee

---
## AI
---


The average lifespan of a chimpanzee is between 40 to 50 years in the wild, and up to 60 years in captivity.
```

### Multi-line Inputs

`ezGPT` also supports multiline inputs when executing the script without arguments or when responding.

By default, `ezGPT` will send the request once three empty lines have been entered.

```
[anon:~]$ gpt

---
## User
---
please
print
hello world



---
## AI
---
Hello World

---
## User
---
change the
second word to 'GPT'



---
## AI
---
Hello GPT
```

## Configuration

The following values are configurable by changing the values in the script:
- `MODEL`
- `NUM_EMPTY_LINES_TO_SEND_REQUEST`
- `SYSTEM_MESSAGE`
- `TEMPERATURE`

## Logging

All conversations are stored in `/path/to/cloned/repository/logs` as separate markdown files.