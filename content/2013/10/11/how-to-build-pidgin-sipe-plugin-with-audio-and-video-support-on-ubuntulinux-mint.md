---
title: How to build pidgin-sipe plugin with audio and video support on ubuntu/linux mint
description: 
date: 2013-10-11T16:37:49
slug: how-to-build-pidgin-sipe-plugin-with-audio-and-video-support-on-ubuntulinux-mint
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - pidgin
  - sipe
---


Tested with [pidgin-sipe-1.17.0](https://sourceforge.net/projects/sipe/files/sipe/)

First of all install dependencies: 
```bash
sudo apt-get install \
    libxml2-dev \
    libnspr4-dev \
    libnss3-dev \
    libgstreamer0.10-dev \
    libnice-dev \
    libpurple-dev \
    libnss3-dev \
    libglib2.0-dev
```

Then check where `libnspr4` was installed:
```bash
sudo dpkg -L libnspr4
```

Then finally configure `nspr` paths accordingly, compile and install it: 

```bash
./configure \
    --prefix=/usr \
    --with-vv \
    --with-nss-includes=/usr/include/nss \
    --with-nss-libs=/usr/lib/x86_64-linux-gnu \
    --with-nspr-includes=/usr/include/nspr \
    --with-nspr-libs=/usr/lib/x86_64-linux-gnu 
make 
sudo make install
```

Hope it helps :) 

If everything works fine then your `Lync` contact list should look like this: 

{{< figure src="../pidgin-sipe-1-17-0.png" title="pidgin with sipe-1.17.0" >}}
