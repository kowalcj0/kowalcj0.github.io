---
title: "Fix an issue with incorrectly transferred files via GSConnect"
description: "by adding custom iptables rules to your Android firewall app"
date: 2021-09-25T22:09:22+01:00
draft: true
toc: false
slug: "fix-file-transfers-for-gsconnect"
categories:
  - unix
  - android
tags:
  - gsconnect
  - afwall
  - firewall
  - iptables
cover:
  image: ../afwall.png
  caption: "SRC: https://github.com/ukanth/afwall/blob/beta/playstore/playstore.png"
  style: normal
---

I've recently flashed LingeageOS 18.1 onto my phone. After rooting it, I've installed 
my fav firewall app [AFWall+](https://github.com/ukanth/afwall).
But since then I was having problems with sending files to my pc or other phones via
(GSConnect app)[https://github.com/GSConnect/gnome-shell-extension-gsconnect].
All sent files had different size than the original file on my phone.
I've described it in this [bug report comment](https://github.com/GSConnect/gnome-shell-extension-gsconnect/issues/1157#issuecomment-927181929).

After a bit of reading I realised that I have to add some extra iptables rules 
described in [GSConnect's Wiki](https://github.com/GSConnect/gnome-shell-extension-gsconnect/wiki/Help#iptables), 

Once, I've added those rules to `AFWall+` then everything started to work as expected.

If you're having similar issue and you're using `AFWall+` then **PLEASE** read their 
tutorial on [Loading scripts from files](https://github.com/ukanth/afwall/wiki/CustomScripts#loading-scripts-from-files) first. 

In my case, I've created a script called `gsconnect-iptables.sh` with following rules:

```bash
# Necessary at the beginning of each script!
IP6TABLES=/system/bin/ip6tables
IPTABLES=/system/bin/iptables
# Open port 1714 to 1764 for GSConnect
$IPTABLES -I "afwall-wifi" -p udp --dport 1714:1764 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -I "afwall-wifi" -p tcp --dport 1714:1764 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A "afwall-wifi" -p tcp --sport 1714:1764 -m state --state NEW,ESTABLISHED -j ACCEPT
$IPTABLES -A "afwall-wifi" -p udp --sport 1714:1764 -m state --state NEW,ESTABLISHED -j ACCEPT
```

Then in the "**Set custom script**" menu option I specified the path to the script 
preceded by a dot command:

```bash
. /path/to/gsconnect-iptables.sh
```

After going to airplane mode, I re-applied the firewall rules and turned the airplane 
mode off.  
Since then, I haven't had any issues with file transfers :)

