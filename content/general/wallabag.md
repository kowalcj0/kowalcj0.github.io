---
draft: false
title: "Wallabag"
description: "Asorted articles I've amassed in Wallabag"
toc: false
slug: "wallabag"
date: "2020-05-02T16:56:52+01:00"
categories:
  - general
tags:
  - links
cover:
  image: /img/logo-wallabag-black.svg
  caption: "SRC: https://wallabag.org/user/themes/boxify/img/logo-wallabag-black.svg"
  style: wide
---

A while ago I've discovered [Wallabag](https://wallabag.org/en). It's a self 
hostable application for saving web pages. 
It extracts the article's content and can automatically tag it with matching
label.
Basically it's an open-source competitor of [Pocket](https://getpocket.com/), 
[Instapaper](https://www.instapaper.com/) or [Evernote](https://evernote.com/).

Fetching a list of all entries via [Wallabag's API](https://app.wallabag.it/api/doc#get--api-entries.{_format}) is very easy.
And with a help of [jq](https://stedolan.github.io/jq/) you can transform it
into a simple JSON file which you can use to populate a Hugo [Data Templates](https://gohugo.io/templates/data-templates/).

```bash
http GET https://{YOUR_WALLABAG_HOST}/api/entries.json?perPage=500 "Authorization:Bearer {API_TOKEN}" |\
    jq '[._embedded.items[] | {title: .title, url: .url}]' |\
    jq 'sort_by(.title)' > entries.json
```

So, without further ado, here's an asorted list of articles I've amassed in Wallabag.


{{< wallabag >}}

