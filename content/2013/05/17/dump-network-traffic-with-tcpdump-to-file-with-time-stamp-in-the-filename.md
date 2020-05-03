---
title: Dump network traffic with tcpdump to file with time-stamp in the filename
description: 
date: 2013-05-17T15:23:00
slug: dump-network-traffic-with-tcpdump-to-file-with-time-stamp-in-the-filename
draft: false
categories:
  - wordpress
  - unix
tags:
  - tcpdump
---

A one-liner that dumps the network traffic into a file with a time-stamp in its name: 

```bash
date +'%Y-%m-%d_%H_%M-%Z' | xargs -I {} bash -c "sudo tcpdump -nq -s 0 -i eth0 -w ./tcpdump-{}.pcap"
```
