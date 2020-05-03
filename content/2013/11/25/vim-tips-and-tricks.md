---
title: Vim - tips and tricks
description: 
date: 2013-11-25T13:04:27
slug: vim-tips-and-tricks
draft: false
categories:
  - wordpress
tags:
  - vim
---

Record a macro that will delete everything after matching character and repeat it N-times. 
In this example we're going to use `=` as the matching character. 

> qaf=D⏎q

Where:
* `qa` - to start recording and save it under 'a' buffer
* `f=` - find '=' character
* `D` - Delete everything to the EOL
* `⏎` - press 'enter' to go to the beginning of next line
* `q` - to stop recording the macro then to repeat the macro N-times, i.e. repeat it 5 times: 

> 5@a

* `5` - the number of times you'd like to repeat the macro
* `@a` - play macro recorded under `a` buffer

{{< 
    figure 
    src="../vim-macro-delete-everything-after-matching-character-and-repeat-n-times1.gif" 
    title="An example of a VIM macro which deletes everything after matching character and is repeated 5 times"
>}}
