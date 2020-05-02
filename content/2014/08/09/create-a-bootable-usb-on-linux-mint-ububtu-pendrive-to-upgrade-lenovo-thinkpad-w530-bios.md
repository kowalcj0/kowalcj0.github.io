---
title: Create a bootable USB pendrive to upgrade Lenovo ThinkPad W530 BIOS
description: 
date: 2014-08-09T14:24:43
slug: create-a-bootable-usb-on-linux-mint-ububtu-pendrive-to-upgrade-lenovo-thinkpad-w530-bios
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - bios
---

Recently I had to update the bios of my laptop from a USB pendrive, 
because I had no CD/DVD drive around. 
Cameron Seader's post [Lenovo BIOS Update method for Linux and USB thumb drive](http://blog.seader.us/2013/10/lenovo-bios-update-method-for-linux-and.html) came very handy, 
but used an obsolete tool so I updated his instructions a bit to make them work. 

### 1. Get the machine type and model of your laptop 

In order to grab this information you can either go to the BIOS or use `dmidecode` or `hwinfo`. 
In my case it was ThinkPad W530 2438-2KU. 

### 2. Download bios update ISO from Lenovo's site 

I got mine: "g5uj22us.iso" from [Lenovo's support page](https://download.lenovo.com/pccbbs/mobiles/g5uj39us.iso)


### 3. Extract the boot image from the iso 

To do it you can use `genisoimage`, which can be installed using regular.

```bash
sudo apt-get install genisoimage
```

PS. you can also download it from: [Ubuntu man pages](https://manpages.ubuntu.com/manpages/focal/en/man1/genisoimage.1.html)

Once you have this tool installed, extract boot image from ISO with: 

```bash
geteltorito g5uj22us.iso > biosupdate.img
```

### 4. Copy the boot image to the USB pendrive

```bash
sudo dd if=biosupdate.img of=/dev/usbthumdrive bs=512K
```

Reboot and boot from USB to run the Flash Utility Cheers,  
Señor QA

