---
draft: true
title: "Build DeadBeef from source"
slug: "build-deadbeef-from-source"
date: "2018-05-04T20:05:50+01:00"
categories:
  - linux
tags:
    - build
cover:
  image: /img/2018/016/deadbeef-logo.png
  caption: "DeadBeef logo. Source: [deblinux](https://deblinux.files.wordpress.com/2012/06/deadbeef-logo.png)"
  style: normal
---

```shell
sudo dnf install \
 libtool \
 jansson \
 jansson-devel \
 flac-devel \
 faad2-libs \
 faad2-devel \
 libmad-devel \
 mac-devel \
 wavpack-devel \
 libvorbis-devel \
 opus-devel \
 libsndfile-devel \
 mac-libs \
 opus \
 alsa-lib \
 alsa-lib-devel \
 faad2-devel \
 libcdio-devel \
 libcddb-devel \
 libjpeg-devel \
 libcurl-devel \
 libvorbis-devel \
 libogg-devel \
 libvorbis libogg \
 ffmpeg-devel \
 yasm \
 yasm-devel \
 gtk3-devel
```


```shell
./configure \
    --enable-threads=posix \
    --enable-m3u \
    --enable-converter \
    --enable-artwork-imlib2 \
    --enable-mono2stereo  \
    --enable-ffap \
    --enable-mp3 \
    --enable-flac \
    --enable-wavpack \
    --enable-cdda \
    --enable-gtk3 \
    --enable-artwork \
    --enable-aac \
    --enable-dca \
    --enable-mms \
    --enable-alac \
    --enable-wma \
    --enable-alsa
```
