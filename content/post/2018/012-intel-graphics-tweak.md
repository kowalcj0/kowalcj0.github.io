---
draft: true
title: Tweaking Intel graphics on linux
slug: "tweaking-intel-graphics-on-linux"
date: "2018-03-15T08:46:10+01:00"
categories:
  - linux
tags:
    - intel
    - driver
---


get info about firmware
```shell
modinfo i915 | grep ^fi
```

List all driver parameters
```
modinfo -p i915
```

If find the output of the above command confusing, as you can't see the actual 
values of every parameter, then use:
```
sudo grep -H '' /sys/module/i915//parameters/*
```

If you see error messages like this one:
```shell
$ dmesg |tail
[ 2360.475430] [drm] not enough stolen space for compressed buffer (need 4325376 bytes), disabling
[ 2360.475437] [drm] hint: you may be able to increase stolen memory size in the BIOS to avoid this
```

then you can enable framebuffer compression. This should also save your laptop
some energy:
```shell
# list all grub menu entries
sudo grubby --info=ALL
# you can also display info about the currently used config with:
sudo grubby --info=0
# to enable FBS, run command below with appropriate kernel version:
sudo grubby --args="i915.enable_fbc=1" --update-kernel /boot/vmlinuz-4.15.10-300.fc27.x86_64
# you can also check if your changes were persisted:
sudo grubby --info=
```

Related reading:

* http://kernel.ubuntu.com/~cking/power-benchmarking/background-colour-and-framebuffer-compression/results.txt
* https://wiki.archlinux.org/index.php/intel_graphics#Framebuffer_compression_.28enable_fbc.29
* https://www.phoronix.com/scan.php?page=article&item=intel_i915_power&num=1
* https://www.phoronix.com/scan.php?page=news_item&px=Intel-FBC-Default-Patch-SKL


Enable GuC / HuC [^1] firmware loading:

* GuC is an engine for workload scheduling of the parallel graphics engines.
* HuC appears to be a firmware blob responsible High Efficiency Video Coding (HEVC / H.265) support.

```shell
sudo grubby --args="i915.enable_guc_loading=1 i915.enable_guc_submission=1" --update-kernel /boot/vmlinuz-4.15.10-300.fc27.x86_64
```

https://wiki.archlinux.org/index.php/intel_graphics#Enable_GuC_.2F_HuC_firmware_loading

[^1]: more info on [phoronix](https://www.phoronix.com/scan.php?page=news_item&px=Intel-Linux-Driver-Getting-HuC)  
