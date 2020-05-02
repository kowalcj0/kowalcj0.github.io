---
title: Getting the Brightness Control to work on Lenovo ThinkPad with Linux Mint 17 (x64) installed and with Nvidia Quadro K1000M on board
description: 
date: 2014-08-10T10:03:30
slug: getting-the-brightness-control-to-work-on-lenovo-thinkpad-with-linux-mint-17-x64-installed-and-with-nvidia-quadro-k1000m-on-board
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - bios
  - nvidia
  - X11
  - grub
---

I haven't had much problems with getting the Brightness Control to work in Mint 16, 
but after installing v17 I had to struggle much more. 

I honestly admit that I don't know which of the following steps actually did the trick, 
nevertheless it works now :) 

OK, I'm currently running Mint 17 x64 on Lenovo W530 with Nvidia Quadro K1000M 
and with Nvidia 331.38 installed. Display mode in BIOS is set to `Discrete Mode`. 

Here's a list of things I did: 


- I've updated the bios to latest available version (G5ET99WW (2.59)) [Here's my tutorial how to upgrade it from a USB pendrive]({{< ref "/2014/08/09/create-a-bootable-usb-on-linux-mint-ububtu-pendrive-to-upgrade-lenovo-thinkpad-w530-bios.md" >}})
- Generated a new `xorg.conf` using "NVIDIA X Server Settings -> X Server Display Configuration -> Save to X Configuration file" 
- Then added `EnableBrightnessControl=1` to the device section in `/etc/X11/xorg.conf`: 

```bash
Section "Device" Identifier "Device0" Driver "nvidia" VendorName "NVIDIA Corporation" BoardName "Quadro K1000M" Option "RegistryDwords" "EnableBrightnessControl=1" EndSection
```

- After rebooting, the only thing I could find in `/sys/class/backlight` was: `thinkpad_screen`
- Then I tried to set the `"GRUB_CMDLINE_LINUX_DEFAULT"` in `/etc/default/grub` to: `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_osi=Linux acpi_backlight=vendor"` or `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nox2apic acpi_osi=Linux acpi_backlight=vendor"` but that didn't work 
- Finally I set it to only: `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nox2apic"`
- and after rebooting Brightness Control buttons (Fn+F8 & F9) started to work and in the `/sys/class/backlight` I found `acpi_video0` instead of `thinkpad_screen` 
```bash
ls -la /sys/class/backlight total 0 lrwxrwxrwx 1 root root 0 Aug 10 10:14 acpi_video0 -> ../../devices/pci0000:00/0000:00:01.0/0000:01:00.0/backlight/acpi_video0/
```

I hope this will help someone. 

Pls drop some comments if it helped you!  
Cheers,  
Señor QA
