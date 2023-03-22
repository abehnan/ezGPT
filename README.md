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
[anon:~/work/ezGPT]$ gpt what is the average lifespan of a chimpanzee
----------------------------------------------------
                   ezGPT started
----------------------------------------------------
----------------------------------------------------
                         AI
----------------------------------------------------


The average lifespan of a chimpanzee in the wild is around 40 to 45 years. However, in captivity, they can live up to 60 years or more.
```

### Multi-line Inputs

`ezGPT` also supports multiline inputs when executing the script without arguments or when responding.

By default, `ezGPT` will send the request once two empty lines have been entered.

This is configurable by changing the `NUM_EMPTY_LINES_TO_SEND_REQUEST` variable.

```
[anon:~/work/ezGPT]$ gpt
----------------------------------------------------
                   ezGPT started
----------------------------------------------------

----------------------------------------------------
                        User
----------------------------------------------------
please
print
hello world


----------------------------------------------------
                 Sending request...
----------------------------------------------------

----------------------------------------------------
                         AI
----------------------------------------------------
Hello world

----------------------------------------------------
                        User
----------------------------------------------------
change
it
to
hello earth


----------------------------------------------------
                 Sending request...
----------------------------------------------------

----------------------------------------------------
                         AI
----------------------------------------------------
Hello earth
```

Note conversations are currently cleared when the script exits.

**i.e.** Permanent storage has not been implemented yet.