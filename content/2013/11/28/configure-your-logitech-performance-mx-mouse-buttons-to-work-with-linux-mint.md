---
title: Configure your Logitech Performance MX Mouse buttons to work with Linux Mint
description: 
date: 2013-11-28T11:50:40
slug: configure-your-logitech-performance-mx-mouse-buttons-to-work-with-linux-mint
draft: false
categories:
  - wordpress
  - unix
tags:
  - linux
  - xbindkeys
---

To make your extra mouse buttons work on Linux Mint (I've tested it with v15) follow all the steps listed in this [tutorial][1] except the step 4 :)

Once you get to step 4, use this key mappings to make the 'zoom' and 'switch between windows' buttons work as on windows. 

```bash
vi $HOME/.xbindkeysrc
...
# show all windows: Scale
"xte 'keydown Control_L' 'keydown Alt_L' 'key Down' 'keyup Control_L' 'keyup Alt_L'"
  b:10 + release

# Zooming with Logitech Performance MX mouse
# thx to: https://www.ralf-oechsner.de/opensource/page/logitech_performance_mx
# Press 'zoom' button and scroll up/down to zoom in/out
# then press the 'zoom' button again to exit from the 'zoom' mode
"xte 'keydown Control_L' &"
   b:13

"xte 'keyup Control_L' &"
   Control + b:13
```

I hope that you'll like Mint even more from now on :)

[1]: http://lotphelp.com/lotp/lotp-guide-logitech-mx-mouse-ubuntu (Using Your Logitech MX Mouse with Ubuntu)