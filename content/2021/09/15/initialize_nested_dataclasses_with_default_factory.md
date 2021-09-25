---
title: "Use default factory to initialize nested dataclass fields"
description: "A quick take on how to avoid problems with nested dataclasses"
date: 2021-09-15T17:50:36+01:00
draft: false
toc: false
slug: "initialize_nested_dataclasses_with_default_factory"
categories:
  - programming
tags:
  - python
---


I you happen to work with nested Python [dataclasses](https://docs.python.org/3/library/dataclasses.html), then maybe you've noticed 
an issues with defining field values by creating an instance of some object. 

In the example below, all instances of class `Main` will point to the same instance 
of class `Sub`:

```python
from dataclasses import dataclass, field

@dataclass
class Sub:
    prop: str = field(default="some value")

@dataclass
class Main:
    sub: Sub = Sub()


m1 = Main()
m2 = Main()

id(m1)
Out[1]: 140304747921264

id(m2)
Out[2]: 140304748528400

assert id(m1.sub) != id(m2.sub)
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-8-63c2e0b3d3f5> in <module>
----> 1 assert id(m1.sub) != id(m2.sub)

AssertionError:
```

The fix is really easy. Simply provide the name of the class you want to instantiate as 
`default_factory` argument to the [field](https://docs.python.org/3/library/dataclasses.html#dataclasses.field) function:

```python
from dataclasses import dataclass, field

@dataclass
class Sub:
    prop1: str = field(default="some value")

@dataclass
class Main:
    sub: Sub = field(default_factory=Sub)

m1 = Main()
m2 = Main()

assert id(m1.sub) != id(m2.sub)
```

This way you'll correctly initialize field values.

