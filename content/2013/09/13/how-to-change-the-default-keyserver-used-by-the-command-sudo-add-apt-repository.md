---
title: How to change the default keyserver used by add-apt-repository
description: 
date: 2013-09-13T13:55:52
slug: how-to-change-the-default-keyserver-used-by-the-command-sudo-add-apt-repository
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - apt
---

If you've encountered problems with connecting to `keyserver.ubuntu.com` like:
```bash
.... 
Executing: 
gpg --ignore-time-conflict --no-options --no-default-keyring --secret-keyring /tmp/tmp.UsuIhHAgLO --trustdb-name /etc/apt//trustdb.gpg --keyring /etc/apt/trusted.gpg --primary-keyring /etc/apt/trusted.gpg --keyserver keyserver.ubuntu.com --recv-keys CFCA9579 
gpg: requesting key CFCA9579 from hkp server keyserver.ubuntu.com 
gpg: keyserver timed out 
gpg: keyserver receive failed: keyserver error
```

Which might show up after you've added a new ppa to your list of repositories using `add-apt-repository`  
i.e.: "`sudo add-apt-repository ppa:jon-severinsson/ffmpeg`" 


Then what you have to do is to change the default port used for obtaining pgp keys from `11371` to `80`.  
To do this, edit `/usr/lib/linuxmint/mintSources/mintSources.py` and replace all the occurrences of "`keyserver.ubuntu.com`" with `hkp://keyserver.ubuntu.com:80`

after that,  
...  
simply enjoy the rest of your life!

Tested on linux mint 15.
