---
draft: false
title: "Listen to podcasts in MPD"
description: "A simple script to load N-recent episodes of your favourite
podcasts into MPD"
slug: "listen-to-podcasts-in-mpd"
date: "2020-03-22T12:02:34+01:00"
categories:
  - unix
tags:
  - linux
  - mpd
  - rss
cover:
  image: ../images/rss_to_mpd.png
  caption: "ASCII art generated with http://patorjk.com/software/taag/ & colored with http://patorjk.com/text-color-fader/"
  style: normal
---


## Requirements

* [mpd](https://www.musicpd.org/) & [mpc](https://www.musicpd.org/clients/mpc/)
* a list of podcast RSS feed links


# Example podcast RSS feed links

Here's list of my favourite English & Polish podcasts in an [OPML](../files/podcasts.opml)
format.

You can extract RSS feed links from it with:

```shell
awk -F '"' '{print $6}' podcasts.opml | sed '/^$/d'
```


## Load podcast into MPD

Given that you've saved your podcast feed list in `~/Music/podcasts.rss`.  
Then with a simple while loop you can load your podcast episodes into mpd.

Add this to your `~/.bashrc` or `~/.bash_profile`:
```shell
alias podcasts=fetch_last_n_episodes

function fetch_last_n_episodes() {
    N="${1:-5}"  # defaults to 5 most recent episodes
    mpc --quiet clear
    while read rss; do
        mpc load --quiet --wait --range=0:${N} ${rss}
    done <~/Music/podcasts.rss
    mpc --quiet random
    mpc --quiet play
}
```

Then run `podcasts`, wait a bit and enjoy your fav podcasts.


### Notes

* If you get rid of `--range=0:${N}` then all episodes from all feeds will be loaded
* `--wait` is optional, and should make things lil bit more stable

