---
draft: false
title: "Convert old mov files to more modern mp4 x264 or AV1"
description: "Make you old videos watchable"
slug: "convert-mov-to-mp4-or-av1"
date: "2020-03-21T11:59:50+01:00"
categories:
  - unix
tags:
  - linux
  - ffmpeg
  - codecs
cover:
  image: ../images/1920px-AV1_logo_2018.png
  caption: "AV1 FTW!. src: https://commons.wikimedia.org/wiki/File:AV1_logo_2018.svg"
  style: normal
---

Some time ago I've discovered a bunch of old QuickTime files on my NAS.
None of those clips could be played back via NextCloud's browser player 
as they were encoded with old school
[mjpeg](https://en.wikipedia.org/wiki/Motion_JPEG) video codec & low quality 
mono pcm_s16be audio.

This is what `mediainfo` told me about those files:
```md
Video
Format                 : JPEG
Codec ID               : jpeg
Bit rate mode          : Variable
Bit rate               : 3 827 kb/s
Width                  : 640 pixels
Height                 : 480 pixels
Display aspect ratio   : 4:3
Frame rate mode        : Constant
Frame rate             : 30.000 FPS
Color space            : YUV
Chroma subsampling     : 4:2:2
Bit depth              : 8 bits
Compression mode       : Lossy
Bits/(Pixel*Frame)     : 0.415
...
Audio
Bit rate mode          : Constant
Bit rate               : 128 kb/s
Channel(s)             : 1 channel
Sampling rate          : 7 840 Hz
Bit depth              : 16 bits
```


I've decided to transcode them to hopefully a future-proof format.
After a bit of testing I've decided to stick with x264 and Opus @ cfr 18 as it:

* provided v.good visual quality
* transcocding is pretty fast
* is recognised by most of the video players (including browsers)
* can be streamed nicely

I also decided to upsample the audio, so it can be easily mixed & edited during
video editing.

Converting those file to AV1 deemed to be pointless as the file size savings 
are not worth the transcoding times. On average it took more than 45 minutes to
transcode a 45s mov file described earlier!!!


# File size comparison

* Original file: 22,890,348 bytes

| -c:v       | profile     | -c:a | File size   | video   | audio  |
| ---------- | ----------- | ---- | ----------- | ------- | ------ |
| libx264    | -crf 10     | aac  | 24,368,779B | 23042kB | 730kB  |
| libx264    | -crf 10     | mp3  | 24,727,469B | 23042kB | 1067kB |
| libx264    | -crf 10     | opus | 24,511,013B | 23042kB | 868kB  |
| libx264    | -crf 18     | aac  | 10,118,378B |  9126kB | 730kB  |
| libx264    | -crf 18     | mp3  | 10,477,856B |  9126kB | 1067kB |
| libx264    | -crf 18     | opus | 10,260,612B |  9126kB | 868kB  |
| libaom-av1 | constant    | opus |  1,439,833B |      kB | 868kB  |
| libaom-av1 | constrained | opus |  8,113,605B |  7217kB | 697kB  |
| libaom-av1 | 2-pass      | opus | 13,537,391B | 12329kB | 868kB  |


# x264 crf 10 & mp3

```shell
ffmpeg \
    -i input.mov \
    -vcodec libx264 \
    -preset slow \
    -tune film \
    -crf 10 \
    -c:a libmp3lame \
    -ar 48000 \
    -ac 2 \
    -b:a 192k \
    output_mp3.mp4
```

# x264 crf 10 & aac

```shell
ffmpeg \
    -i input.mov \
    -vcodec libx264 \
    -preset slow \
    -tune film \
    -crf 10 \
    -c:a aac \
    -ar 48000 \
    -ac 2 \
    -b:a 192k \
    output_aac.mkv
```

# x264 crf 10 & Opus
```shell
ffmpeg \
    -i input.mov \
    -vcodec libx264 \
    -preset slow \
    -tune film \
    -crf 10 \
    -c:a libopus \
    -ac 2 \
    -ar 48000 \
    -b:a 192000 \
    output_opus.mkv
```


# AV1 & Opus

Unfortunately I wasn't able to convert mov files directly to AV1, so I used 
the `output_opus.mkv` from previous example.


## Constant quality

```shell
ffmpeg \
    -i output_opus.mkv \
    -c:v libaom-av1 \
    -crf 30 \
    -b:v 0 \
    -strict experimental \
    -c:a copy \
    av1_constant.mkv
```


## Constrained quality

```shell
ffmpeg \
    -i output_opus.mkv \
    -c:v libaom-av1 \
    -minrate 500k \
    -b:v 2000k \
    -maxrate 2500k \
    -strict experimental \
    -c:a copy \
    av1_constrained.mkv
```


## 2-Pass

```shell
ffmpeg \
    -y \
    -i output_opus.mkv \
    -c:v libaom-av1 \
    -strict -2 \
    -b:v 2000K \
    -maxrate 2500K \
    -pass 1 \
    -f matroska NUL \
    && \ 
fmpeg \
    -i output_opus.mkv \
    -c:v libaom-av1 \
    -strict -2 \
    -b:v 2000K \
    -maxrate 2500K \
    -pass 2 \
    -c:a copy \
    av1_2pass.mkv
```


# Sources:

* https://www.streamingmedia.com/Articles/ReadArticle.aspx?ArticleID=130284
* https://ffmpeg.org/ffmpeg-codecs.html
* https://trac.ffmpeg.org/wiki/Encode/AV1

