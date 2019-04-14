---
draft: false
title: "Fix 'X11 connection broke' issue in QT based GUI applications like VLC"
description: "Fix it by setting QT_AUTO_SCREEN_SCALE_FACTOR env var"
slug: "vlc-auto-screen-scale-factor-issue"
date: "2018-02-11T22:40:50+01:00"
categories:
  - linux
tags:
    - vlc
    - qt

featuredImage: /img/2018/007/vlc.png
featuredImageDescription: troublesome VLC
dropCap: false
---
If you ever encountered error like this when starting vlc:

```shell
$ vlc
VLC media player 3.0.0-rc5 Vetinari (revision 3.0.0-rc5-0-gf53236af09)
[0000560cfbe38410] main libvlc: Running vlc with the default interface. Use 'cvlc' to use vlc without interface.
The X11 connection broke: Maximum allowed requested length exceeded (code 4)
XIO:  fatal IO error 22 (Invalid argument) on X server ":0"
      after 447 requests (447 known processed) with 0 events remaining.
QMutex: destroying locked mutex
```

Then you can fix it by setting the `QT_AUTO_SCREEN_SCALE_FACTOR` env variable to `0`, i.e.:

```shell
QT_AUTO_SCREEN_SCALE_FACTOR=0 vlc your_video_file.mkv
```

You can also modify the `.desktop` file so that this variable is always set,
when you start the application via e.g. apps menu:
In `/usr/share/applications/vlc.desktop` replace:

```shell
Exec=/usr/bin/vlc --started-from-file %U
```

with:

```shell
Exec=env QT_AUTO_SCREEN_SCALE_FACTOR=0 /usr/bin/vlc --started-from-file %U
```

and Bob's your uncle.
