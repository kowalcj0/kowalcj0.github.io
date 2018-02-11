---
draft: false
title: "Allow GUI applications run by root user to connect to X server"
slug: "allow-application-run-by-root-to-connect-to-x-server"
date: "2018-02-04T13:46:30+01:00"
categories:
  - linux
tags:
  - root
  - wayland
  - fedora 27
  - gnome 3.26
cover:
  image: /img/2018/005/Wayland_Logo-wiki.png
  caption: Wayland logo
  style: normal
---

Recently I had an annoying problem running Wireshark as root user on Fedora 27 
(Wayland + Gnome 3.26).  
I was getting following error:
```bash
sudo wireshark
QStandardPaths: XDG_RUNTIME_DIR not set, defaulting to '/tmp/runtime-root'
QXcbConnection: Could not connect to display
Aborted (core dumped)
```

To fix this, you need to add `root` user to the list of users allowed to make 
connections to the X server. 
```bash
xhost si:localuser:root
```

That's it. From now on, you shouldn't have any problems running GUI
applications by root user.

For more info on debuging Wayland problems please refer to [Fedora's wiki page](https://fedoraproject.org/wiki/How_to_debug_Wayland_problems)

PS. `xprop` tool, described in the aforementioned wiki page, has a cool feature 
to display application icon as ASCII art :)
Here's for example [Vivaldi's](https://vivaldi.com/) icon:

```bash

	  ░▒▒▒▒▒▒▒▒▒▒░
	 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒
	░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
	▒▒▒░░▒▒▒▒▒░░▒▒▒▒
	▒▒▒  ░▒▒▒▒  ░▒▒▒
	▒▒░   ▒▒▒▒  ░▒▒▒
	▒▒▒   ░▒▒▒  ▒▒▒▒
	▒▒▒░   ░▒░ ░▒▒▒▒
	▒▒▒▒       ▒▒▒▒▒
	▒▒▒▒░     ░▒▒▒▒▒
	▒▒▒▒▒     ▒▒▒▒▒▒
	▒▒▒▒▒▒   ▒▒▒▒▒▒▒
	▒▒▒▒▒▒░░░▒▒▒▒▒▒▒
	░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
	 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒
	  ░▒▒▒▒▒▒▒▒▒▒░
```
