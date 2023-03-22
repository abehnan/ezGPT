# ezGPT
This a simple terminal-based chatGPT chatbot.

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

By default, `ezGPT` will send the request once three lines have been entered.

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

Note conversations are currently cleared when the script exits.

**i.e.** Permanent storage has not been implemented yet.

## Configuration

The following values are configurable by changing the values at the beginning of the script.
- `API_URL`
- `MODEL`
- `NUM_EMPTY_LINES_TO_SEND_REQUEST`
- `SYSTEM_MESSAGE`
- `TEMPERATURE`