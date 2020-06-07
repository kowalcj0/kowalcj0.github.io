---
title: "UrlString"
description: "Easily build URL strings with / syntax"
date: 2020-05-14T14:10:00+01:00
draft: false
slug: "python-url-strings"
toc: false
categories:
  - programming
tags:
  - python
---

[UrlString](https://github.com/uktrade/directory-constants/blob/a35f94da3ee022b96b97ebccc84205d66427f753/directory_constants/helpers.py#L17) is a convenience wrapper around a string object for making it easy to build URL strings.
It borrows the `/` syntax from [pathlib](https://github.com/python/cpython/blob/83a9ba442662c2a030b45955f3dd24ff4b24bb61/Lib/pathlib.py#L929) to allow for the building of natural looking URLs.

An example implementation by UK Trade team:
```python
class UrlString(str):
    def __truediv__(self, other):
        base = self.strip('/')
        path = other.strip('/')
        return UrlString(f'{base}/{path}/')
```

Usage:
```python
home = UrlString('https://example.com')
new_url = home / 'foo' / 'bar'
print(new_url)
https://example.com/foo/bar/
```

