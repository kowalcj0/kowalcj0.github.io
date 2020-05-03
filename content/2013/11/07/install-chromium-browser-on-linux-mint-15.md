---
title: How to add official Chromium-browser PPA repository to Linux Mint 15 and install the latest stable build
description: 
date: 2013-11-07T13:59:41
slug: install-chromium-browser-on-linux-mint-15
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - chromium
---

Here's the official Chromium-browser PPA: https://launchpad.net/~chromium-daily/+archive/stable

To install latest stable build follow 3 simple steps: 

1. add "`deb http://ppa.launchpad.net/chromium-daily/stable/ubuntu raring main`" to `/etc/apt/sources.list`
2. add repo's pub key so that we can avoid problems like the one below:
    ```bash
    W: GPG error: http://ppa.launchpad.net raring 
    Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 5A9BF3BB4E5E17B5
    ```

    ```bash
    sudo gpg \
        --keyserver hkp://keys.gnupg.net:80 \
        --recv 5A9BF3BB4E5E17B5
    sudo gpg \
        --export FBEF0D696DE1C72BA5A835FE5A9BF3BB4E5E17B5 |\
            sudo apt-key add -
    ```

    btw. using `hkp://keys.gnupg.net:80` will work even if you're behind a firewall or proxy :) 

3. Update package list and install Chromium

    ```bash
    sudo apt-get update
    sudo apt-get install chromium-browser
    ```

Happy browsing :)