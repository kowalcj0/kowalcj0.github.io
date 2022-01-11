---
title: "How to resolve Pytest: Cell Var From Loop"
description: "How to resolve Pytest: Cell Var From Loop"
date: 2021-12-07T11:43:28Z
draft: false
toc: false
slug: "how-to-resolve-pytest-cell-var-from-loop"
categories:
  - programming
tags:
  - python
---

Recently, I came across following `pylint` warning:

```shell
$ pylint test.py
************* Module test
test.py:29:28: W0640: Cell variable sort_key defined in loop (cell-var-from-loop)

------------------------------------------------------------------
Your code has been rated at 9.41/10 (previous run: 9.41/10, +0.00)
```

Here's an example code snippet that triggered such warning:

```python
"""Replace lambda with operator.itemgetter to sort List[dict] by dict key."""
import itertools
from typing import Dict, List


def parse_raw_message(msg: str) -> Dict[str, str]:
    """Parse a pipe-delimited message into a key:value pairs & skip empty keys."""
    split_messages = msg.split("|")
    iter_chunk_size = 2
    args = [iter(split_messages)] * iter_chunk_size
    return {
        key: value
        for key, value in itertools.zip_longest(*args, fillvalue=None)
        if key
    }


def parse_and_group(
    raw_messages: Dict[str, List[Dict[str, str]]], sorting_keys: Dict[str, str]
) -> Dict[str, List[Dict[str, str]]]:
    """Parse raw messages into a dict and sort them by a specific key."""
    parsed_messages: Dict[str, List[Dict[str, str]]] = {}

    for message_type, messages in raw_messages.items():
        sort_key = sorting_keys[message_type]

        parsed_messages[message_type] = sorted(
            (parse_raw_message(msg) for msg in messages),
            key=lambda d: d[sort_key]
        )

    return parsed_messages


if __name__ == "__main__":
    some_raw_messages = {
        "a": [
            "key_a|3|b|2|c|o",
            "key_a|2|b|3|c|f",
            "key_a|1|b|4|c|g",
        ],
        "b": [
            "key_b|2|b|2|c|o",
            "key_b|3|b|1|c|h",
            "key_b|1|b|0|c|j",
        ],
    }
    some_sorting_keys = {
        "a": "key_a",
        "b": "key_b",
    }
    print(parse_and_group(some_raw_messages, some_sorting_keys))
```

The warning is triggered for the nested `lambda` function:
```python
        parsed_messages[message_type] = sorted(
            (parse_raw_message(msg) for msg in messages),
            key=lambda d: d[sort_key]
        )
```
which looks up variables from the parent scope when executed, not when defined. This is nicely explained by [Martijn Pieters](https://stackoverflow.com/a/12423750).

As it turned out, it's a false positive warning, which [I reported](https://github.com/PyCQA/pylint/issues/5508).  
It was also [reported in the past](https://github.com/PyCQA/pylint/issues/3107).

To get rid of this warning, we have to replace `lambda` with `operator.itemgetter()`:

```python
import operator

...
        parsed_messages[message_type] = sorted(
            (parse_raw_message(msg) for msg in messages),
            key=operator.itemgetter(sort_key)
        )
...
```


