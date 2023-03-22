# ezGPT
This a simple terminal-based chatGPT chatbot.

## Setup

In `~/.bashrc`:

```
export OPENAI_API_KEY='<YOUR_OPENAI_KEY_HERE>'
alias gpt='python /path/to/cloned/repository/ezGPT.py'
```

## Usage

You can prompt gpt direcly from your terminal by preprending your prompt with `gpt.`

```
[anon:~/work/ezGPT]$ gpt what is the average lifespan of a chimpanzee
----------------------------------------------------
                 ezGPT started.
----------------------------------------------------
----------------------------------------------------
                     AI
----------------------------------------------------
The average lifespan of a chimpanzee is around 40-50 years in the wild and up to 60 years in captivity.
```

### Multi-line Inputs

`ezGPT` also supports multiline inputs when executing the script without arguments or when responding.

By default, `ezGPT` will send the request once two empty lines have been entered.

This is configurable by changing the `NUM_EMPTY_LINES_TO_SEND_REQUEST` variable.

```
[anon:~/work/ezGPT]$ gpt
----------------------------------------------------
                 ezGPT started.
----------------------------------------------------

----------------------------------------------------
                      User
----------------------------------------------------
please
print
hello
world


----------------------------------------------------
               Sending request...
----------------------------------------------------

----------------------------------------------------
                     AI
----------------------------------------------------
The code to print "hello world" in Python is:

print("hello world")

----------------------------------------------------
                      User
----------------------------------------------------
now
change
it
to "hello earth"


----------------------------------------------------
               Sending request...
----------------------------------------------------

----------------------------------------------------
                     AI
----------------------------------------------------
To print "hello earth" instead of "hello world", you can simply modify the string argument passed to the `print()` function. Here's the updated code:


print("hello earth")

```

Note conversations are currently cleared when the script exists. i.e. Permanent storage has not been implemented.