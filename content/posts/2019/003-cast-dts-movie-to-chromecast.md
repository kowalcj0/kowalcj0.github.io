---
draft: false
title: "Play moview with DTS audio on Chromecast"
description: "Never give up"
slug: "cast-dts-movie-to-chromecast"
date: "2019-06-09T20:35:50+01:00"
categories:
  - linux
tags:
  - castnow
  - ffmpeg
cover:
  image: ../images/FFmpeg-Logo.svg
  caption: "FFmpeg-Logo by Wikimedia https://commons.wikimedia.org/wiki/File:FFmpeg-Logo.svg"
  style: wide
---

According to the official [specification](https://developers.google.com/cast/docs/media) 
Chromecast (even Ultra version) doesn't support DTS.

If you can't be bothered to spend few hours to transcode the movie with lets
say [Handbrake](https://handbrake.fr/) you can use ver handy CLI casting tool: [castnow](https://github.com/xat/castnow).

Once installed, simply tell it to use ffmpeg to transcode audio to mp3 (or ac3
or aac).

```shell
castnow your-wonderful-movie.mkv \
    --tomp4 \
    --ffmpeg-vcodec copy \
    --ffmpeg-acodec mp3 \
    --ffmpeg-movflags frag_keyframe+empty_moov+faststart
```

* - use `movflags` if you will only hear the audio and you'll see a black screen

The only downside of transcoding is that the play / pause controls are not supported.

