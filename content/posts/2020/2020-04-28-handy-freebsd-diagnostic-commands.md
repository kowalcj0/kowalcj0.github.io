---
draft: false
title: "FreeNas/FreeBSD hardware/diagnostic tools"
description: "A brief overview of various CLI tools that can help you diagnose your FreeBSD system"
slug: "handy-freebsd-diagnostic-tools"
date: "2020-03-28T22:02:34+01:00"
toc: true
toc_levels: 1
categories:
  - freebsd
tags:
  - freenas
  - cli
cover:
  image: ../images/RGB_FreeNAS_Shark_Logo_Onlight_Lg.png
  caption: "SRC: https://www.freebsdnews.com/wp-content/uploads/RGB_FreeNAS_Shark_Logo_Onlight_Lg.png"
  style: normal
---


Handy CLI tools that might help your with diagnosing/debugging issues on your
FreeBSD/FreeNAS machine.


# Recommended reading

* FreeNAS documentation on CLI tools: https://www.ixsystems.com/documentation/freenas/11.3-U2/cli.html
* FreeBSD Display Information About The System Hardware: https://www.cyberciti.biz/tips/freebsd-display-information-about-the-system.html



# camcontrol

The [camcontrol](https://www.freebsd.org/cgi/man.cgi?query=camcontrol) utility is designed to provide a way for users to access
and control the FreeBSD CAM subsystem.

```bash
# camcontrol devlist
<ST4000VN003-1T5168 SC46>          at scbus0 target 0 lun 0 (pass0,ada0)
<ST4000VN003-1T5168 SC46>          at scbus1 target 0 lun 0 (pass1,ada1)
<ST4000VN003-1T5168 SC46>          at scbus2 target 0 lun 0 (pass2,ada2)
<ST4000VN003-1T5168 SC46>          at scbus2 target 0 lun 0 (pass3,ada3)
<ST4000VN003-1T5168 SC46>          at scbus4 target 0 lun 0 (pass4,ada4)
<ST4000VN003-1T5168 SC46>          at scbus5 target 0 lun 0 (pass5,ada5)
<ST4000VN003-1T5168 SC46>          at scbus5 target 0 lun 0 (pass6,ada6)
<ST4000VN003-1T5168 SC46>          at scbus5 target 0 lun 0 (pass7,ada7)
<SanDisk Dual Drive 1.00>          at scbus9 target 0 lun 0 (pass8,da0)
```

# dmesg

The [dmesg](https://www.freebsd.org/cgi/man.cgi?query=dmesg) utility displays the contents of the system message buffer.

To show only CPU model & some basic details:
```bash
dmesg | grep "^CPU"
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
```

For more details use `dmesg | grep CPU` or `dmesg | grep -i cpu`:
```bash
dmesg | grep CPU
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
FreeBSD/SMP: Multiprocessor System Detected: 4 CPUs
SMP: AP CPU #3 Launched!
SMP: AP CPU #2 Launched!
SMP: AP CPU #1 Launched!
cpu0: <ACPI CPU> on acpi0
cpu1: <ACPI CPU> on acpi0
cpu2: <ACPI CPU> on acpi0
cpu3: <ACPI CPU> on acpi0
amdtemp0: <AMD CPU On-Die Thermal Sensors> on hostb7
pmc: Unknown AMD64 CPU.
pmc: Unknown AMD CPU.
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
FreeBSD/SMP: Multiprocessor System Detected: 4 CPUs
SMP: AP CPU #2 Launched!
SMP: AP CPU #3 Launched!
SMP: AP CPU #1 Launched!
cpu0: <ACPI CPU> on acpi0
cpu1: <ACPI CPU> on acpi0
cpu2: <ACPI CPU> on acpi0
cpu3: <ACPI CPU> on acpi0
amdtemp0: <AMD CPU On-Die Thermal Sensors> on hostb7
pmc: Unknown AMD64 CPU.
pmc: Unknown AMD CPU.
CPU: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G (4189.60-MHz K8-class CPU)
```


To find out more about NICs, first list interface names with `ifconfig`, then
grep through dmesg out:
```bash
dmesg | grep em0
em0: <Intel(R) PRO/1000 Legacy Network Connection 1.1.0> port 0xe000-0xe03f mem 0xfea40000-0xfea5ffff,0xfea20000-0xfea3ffff irq 20 at device 5.0 on pci2
...
```

# dmidecode

[dmidecode](https://www.freebsd.org/cgi/man.cgi?query=dmidecode) is a tool for dumping a computer's DMI (some say SMBIOS) table 
contents in a human-readable format.

```bash
dmidecode -h
Usage: dmidecode [OPTIONS]
Options are:
 -d, --dev-mem FILE     Read memory from device FILE (default: /dev/mem)
 -h, --help             Display this help text and exit
 -q, --quiet            Less verbose output
 -s, --string KEYWORD   Only display the value of the given DMI string
 -t, --type TYPE        Only display the entries of given type
 -H, --handle HANDLE    Only display the entry of given handle
 -u, --dump             Do not decode the entries
     --dump-bin FILE    Dump the DMI data to a binary file
     --from-dump FILE   Read the DMI data from a binary file
     --no-sysfs         Do not attempt to read DMI data from sysfs files
     --oem-string N     Only display the value of the given OEM string
 -V, --version          Display the version and exit
```

Useful commands:

* `dmidecode -t processor`
* `dmidecode -t memory`
* `dmidecode -t bios`
* `dmidecode -t baseboard`


# freebsd-version

[freebsd-version](https://www.freebsd.org/cgi/man.cgi?query=freebsd-version) – print the version and patch level of the installed system.

```bash
# freebsd-version
11.3-RELEASE-p6
```


# freenas-debug

[freenas-debug](https://www.ixsystems.com/documentation/freenas/11.3-U2/cli.html#freenas-debug) is a command line utility to show debugging information.
It offers a really fine level of details.

```shell
# freenas-debug
Usage: /usr/local/bin/freenas-debug <options>
Where options are:

    -A	Dump all debug information
    -B	Dump System Configuration Database
    -C	Dump SMB Configuration
    -I	Dump IPMI Configuration
    -M	Dump SATA DOMs Information
    -N	Dump NFS Configuration
    -S	Dump SMART Information
    -T	Loader Configuration Information
    -Z  Remove old debug information
    -a	Dump Active Directory Configuration
    -e	Email debug log to this comma-delimited list of email addresses
    -f	Dump AFP Configuration
    -g	Dump GEOM Configuration
    -h	Dump Hardware Configuration
    -i	Dump iSCSI Configuration
    -j	Dump Jail Information
    -l	Dump LDAP Configuration
    -n	Dump Network Configuration
    -s	Dump SSL Configuration
    -t	Dump System Information
    -y	Dump Sysctl Configuration
    -z	Dump ZFS Configuration
```

# gpart

The [gpart](https://www.freebsd.org/cgi/man.cgi?query=gpart) utility is used to partition GEOM providers, normally disks.

```bash
# gpart show
=>        34  7814037101  ada0  GPT  (3.6T)
          34          94        - free -  (47K)
         128     4194304     1  freebsd-swap  (2.0G)
     4194432  7809842696     2  freebsd-zfs  (3.6T)
  7814037128           7        - free -  (3.5K)

=>        34  7814037101  ada1  GPT  (3.6T)
          34          94        - free -  (47K)
         128     4194304     1  freebsd-swap  (2.0G)
     4194432  7809842696     2  freebsd-zfs  (3.6T)
  7814037128           7        - free -  (3.5K)

=>        34  7814037101  ada2  GPT  (3.6T)
          34          94        - free -  (47K)
         128     4194304     1  freebsd-swap  (2.0G)
     4194432  7809842696     2  freebsd-zfs  (3.6T)
  7814037128           7        - free -  (3.5K)
  ...
  ...
```

# pciconf

The [pciconf](https://www.freebsd.org/cgi/man.cgi?query=pciconf) utility provides a command line interface to functionality 
provided by the pci ioctl interface.

Use `pciconf -lv` to list all known devices with vendor, device, class 
and subclass identification strings loaded from the vendor/device information 
database.

```bash
# pciconf -lv
hostb0@pci0:0:0:0:	class=0x060000 card=0x85cb1043 chip=0x14221022 rev=0x00 hdr=0x00
    vendor     = 'Advanced Micro Devices, Inc. [AMD]'
    device     = 'Family 15h (Models 30h-3fh) Processor Root Complex'
    class      = bridge
    subclass   = HOST-PCI

...
...
...

em0@pci0:2:5:0:	class=0x020000 card=0x13768086 chip=0x107c8086 rev=0x05 hdr=0x00
    vendor     = 'Intel Corporation'
    device     = '82541PI Gigabit Ethernet Controller'
    class      = network
    subclass   = ethernet
re0@pci0:4:0:0:	class=0x020000 card=0x85541043 chip=0x816810ec rev=0x0c hdr=0x00
    vendor     = 'Realtek Semiconductor Co., Ltd.'
    device     = 'RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller'
    class      = network
    subclass   = ethernet
```

# sysctl

The [sysctl](https://www.freebsd.org/cgi/man.cgi?query=sysctl) utility retrieves kernel state and allows processes with 
appropriate privilege to set kernel state.

Basic CPU info:
```bash
# sysctl -a hw.model
hw.model: AMD A10-7870K Radeon R7, 12 Compute Cores 4C+8G
```

To find out more about CPU:
```bash
# sysctl -a | grep -i hw.*cpu
hw.ncpu: 4
hw.vmm.bhyve_xcpuids: 0
hw.vmm.topology.cpuid_leaf_b: 1
hw.acpi.cpu.cx_lowest: C2
dev.hwpstate.0.%parent: cpu0
```

And about RAM:
```bash
# sysctl -a | grep -i hw.*mem
hw.physmem: 33179099136
hw.usermem: 22425677824
hw.realmem: 34359738368
hw.pci.host_mem_start: 2147483648
```

Lastly, you can list all the currently available hardware values use:
```bash
sysctl -a hw
```

# zpool

[zpool](https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/zfs-zpool.html) – is a tool to configure ZFS storage pools.

For diagnostic purposes it's enough to know: `zpool status -v` which will show
the status of all pools in your system.


