---
draft: false
title: "Fix 'XDG_RUNTIME_DIR not set' error when runnning Wireshark as root"
slug: "run-wireshark-as-root-on-gnome-3.26-fix-xdg-runtime-dir-error"
date: "2018-02-11T23:08:50+01:00"
categories:
  - linux
tags:
    - wireshark
    - qt
    - gnome
    - wayland
cover:
  image: /img/2018/006/Wireshark_Logo.png
  caption: Wireshark logo
  style: wide
---
In case you encounter error like the one below, when trying to run `Wireshark`
as root (e.g.: on Fedora 27, Gnome 3.26 & Wayland):

```shell
$ sudo wireshark
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'
No protocol specified
qt.qpa.screen: QXcbConnection: Could not connect to display :0
Could not connect to any X display.
```

Then to fix this, you need to add root user to the list of users allowed to
connect oth X11 server:

```shell
xhost si:localuser:root
```

