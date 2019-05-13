---
draft: false
title: "Logrotate your bash history file"
description: "Never loose your command history"
slug: "logrotate-bash-history"
date: "2019-05-13T11:50:50+01:00"
categories:
  - linux
tags:
    - bash
    - logrotate
cover:
  image: ../images/logrotate.png
  caption: "logrotate ASCII art generated with http://patorjk.com/software/taag/ & colored with http://patorjk.com/text-color-fader/"
  style: normal
---

A while ago I decided to take more control over my bash history and I followed 
this advice [https://unix.stackexchange.com/a/48113](https://unix.stackexchange.com/a/48113).  

With time I've tweaked few settings, like ignore lines that start with space, 
and ignore some of the trivial commands like `ls`:
```
export HISTCONTROL=ignoredups:erasedups:ignorespace     # no duplicate entries & lines starting with space
export HISTSIZE=99999999                                # big big history
export HISTFILESIZE=99999999                            # big big history
shopt -s histappend                                     # append to history, don't overwrite it
export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"  # Save and reload the history after each command finishes
HISTIGNORE='ll *:ls *:l:gs:'                            # ignore some commands
```

Nevertheless, every now and then I'd loose the command history, e.g. when 
upgrading the distro. I then discovered [logrotate](https://linux.die.net/man/8/logrotate).
It's a brilliant and easy to use tool for, guess what, log rotation!

In order to rotate your `.bash_history` file simply create a new logrotate 
config file: `/etc/logrotate.d/bashhistory`:
```
/home/YOUR_USERNAME/.bash_history {
    weekly
    missingok
    rotate 5
    size 5000k
    nomail
    notifempty
    create 600 YOUR_USERNAME YOUR_USERNAME
}
```

and you're golden. From now on, when all conditions are met, logrotate will 
create an empty `~/.bash_history` and append current date to archived file,
e.g. `~/.bash_history-20190513`.

