---
title: "Handy Pipewire commands and tools"
description: ""
date: 2022-01-09T13:14:44Z
draft: true
toc: false
slug: "handy-pipewire-commands-and-tools"
categories:
  - unix
tags:
  - pipewire
cover:
  image: ../PipeWire_hero.jpg
  caption: "SRC: https://www.collabora.com/assets/images/about/opensource/heros/PipeWire_hero.jpg"
  style: normal
---

PipeWire provides a nice set of CLI commands and tools to manage and monitor A/V
devices on you machine.
Here's a list of those commands with some usage examples:

* `pw-cli` - The PipeWire Command Line Interface.
    * Examples:
    * `pw-cli dump short Node` - list all input/output nodes and their state.
    * `pw-cli info 0` - inspect the state of the server.
        * Lists useful details like: clock-rate and allowed clock-rates
* `pw-mon` dumps and monitors the state of the PipeWire daemon.
* `pw-metadata` - Monitor, set and delete metadata on PipeWire objects.
    * `pw-metadata -n settings` - list the current settings.
* `pw-dot` can dump a graph of the pipeline, check out the help for how to do this.
* `pw-top` monitors the real-time status of the graph. This is handy to find out what clients are running and how much DSP resources they use.
* `pw-dump` dumps the state of the PipeWire daemon in JSON format. This can be used to find out the properties and parameters of the objects in the PipeWire daemon.
* `pw-link` - List, monitor or link input or output ports, e.g.:
    * `pw-link --input`
    * `pw-link --output`

BTW. you can still use `pactl` command to control "PulseAudio" sound server, e.g.:
* `pactl info` - shows details like server name & version, sink & source names
* `pactl list` - list all clients, cards, their properties, loaded modules etc
* `pactl list short` - same as above but much less verbose

