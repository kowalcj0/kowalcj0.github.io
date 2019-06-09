---
draft: false
title: "Syntax Highlighting in Hugo"
description: "I just learnt that from version 0.28 Hugo comes with a built-in syntax highlighter called Chroma"
slug: "syntax-highlighting-in-hugo"
date: "2018-01-27T22:28:50+01:00"
categories:
  - random
  - learning
tags:
  - hugo
  - syntax
---
# Bye bye Prism. Welcome Chroma.

I just learnt that from version 0.28 Hugo comes with a built-in syntax 
highlighter called [Chroma](https://gohugo.io/content-management/syntax-highlighting/).

It supports syntax highlighting with GitHub flavoured code fences!  
This is more than great!  
Because of this I could quickly get rid of a bit bulky [Prism](http://prismjs.com/) JS syntax highlighter.


# Enable Chroma

Start by choosing your Chrome style from gallery available at [https://help.farbox.com/pygments.html](https://help.farbox.com/pygments.html)  

Then generate a `css` file:
```bash
hugo gen chromastyles --style=pastie > static/css/syntax.css
```

And finally modify your `config.toml`

```toml
pygmentsUseClasses = true
pygmentsUseClassic = false
pygmentsCodefences = true

[params.assets]
customCSS = ["css/syntax.css"]
```

*NOTE:*  

* Setting `pygmentsUseClassic` to `false` will disable old and slower `Pygments`


# Chroma vs Github fences


## Chroma

Among quite a few syntax highlighting configuration options [^1] `Chroma` has 
two very handy ones:

* highlight specific lines and/or ranges
* start line counter from any number


*NOTE:*  
In order to force Hugo to correctly render the example snippet below, I placed 
a space " " between first two curly braces `{{` and lower than sign `<` in the 
first and the last line of the snippet.
```html
{{ < highlight python "linenos=table,hl_lines=1 4-5,linenostart=99" >}}
from time import time

def since_epoch() -> float :
    # some comment
    return time.time()
{{ < / highlight >}}
```


Here's how this snippet renders:  
{{< highlight python "linenos=table,hl_lines=1 4-5,linenostart=99" >}}
from time import time

def since_epoch() -> float :
    # some comment
    return time.time()
{{< / highlight >}}


## Github fences

Below is a sample `python` snippet surrounded with regular Github fences:  
{{< highlight markdown >}}
```python
from time import time

def rettt() -> str :
    return time.time()
```
{{< / highlight >}}

and here's how it looks like after rendering:
```python
from time import time

def rettt() -> str :
    return time.time()
```
[^1]: more info on [official doc page](https://gohugo.io/content-management/syntax-highlighting/#configure-syntax-hightlighter).  
