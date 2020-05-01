---
draft: false
title: Play videoclip for currently playing song in mpv
description: Have you ever wanted to quickly find a videoclip of currently playing song?
slug: "get-song-title-from-dbus-via-mpris2-find-videoclip-with-ddgr-on-youtube-and-play-it-with-mpv"
date: "2018-03-29T15:15:14+01:00"
categories:
  - unix
tags:
  - linux
  - fun
  - python
  - mpv
  - dbus
cover:
  image: /img/2018/012/tuber.png
  caption: Tuber
  style: normal
---

Short demo:
{{< videoloop src="/vid/2018/013/mpd2mpv.mp4" >}}


# Requirements

You'll need:

* python 3.x
* [mpv](https://mpv.io/) video player
* music player that supports [MPRIS2 D-Bus interface](https://specifications.freedesktop.org/mpris-spec/latest/)
    * [mpd](https://www.musicpd.org/) + [mpDris2](https://github.com/eonpatapon/mpDris2)
    * [deadbeef](http://deadbeef.sourceforge.net/) + [mpris2-plugin](https://github.com/Serranya/deadbeef-mpris2-plugin)
* some `D-Bus` packages -> `dbus-devel dbus-python-devel dbus-glib-devel`
* [ddgr]()https://github.com/jarun/ddgr - a CLI client for `DuckDuckGo` 

## System packages
Once you have your player & MPRIS2 installed & configured, install:
```shell
sudo dnf install dbus-devel dbus-python-devel dbus-glib-devel ddgr
```

## Python packages

Next step is to install python packages.
We'll use a virtualenv:
```shell
mkvirtualenv -p python3.6 mpris2yt2mpv
pip install dbus-python mpris2
```
# Getting artist & song title from D-Bus

Below is a simple script that will connect to the current `mpris2` player.
```python
import mpris2
from mpris2 import Player
from mpris2 import get_players_uri

uri = next(get_players_uri())
player = Player(dbus_interface_info={'dbus_uri': uri})

artist = str(player.Metadata["xesam:artist"][0])
title = str(player.Metadata["xesam:title"])

print("{} - {}".format(artist, title))
```

Save this script somewhere, for example in: `mpris2title.py`

When you run it, it will simply print:
```shell
$ python mpris2title.py 
Glass Animals - Gooey
```

# Alias

Finally, create an alias like below:
```shell
alias vid='BROWSER=mpv ddgr -j -w youtube.com `python mpris2title.py`'
```

This command will search `youtube` for the song you're currently playing using 
`ddgr` and open the first result in `mpv` (as it's set as the default `BROWSER`
for `ddgr`).


# Usage

Now, siply run `vid` in your terminal an (if you're lucky) you'll see
videoclip for the currently playing song played in `mpv`.

Ta-da! you can now quicky find videclips from the comfort of your terminal.
