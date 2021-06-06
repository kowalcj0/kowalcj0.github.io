---
title: "Install Photoprism in Truenas Jail"
description: "Install Photoprism in Truenas Jail"
date: 2021-06-05T17:18:24+01:00
draft: false
toc: false
slug: "install-photoprism-in-truenas-jail"
categories:
  - unix
  - photography
tags:
  - truenas
  - photoprism
  - freebsd
cover:
  image: ../preview.jpg
  caption: "SRC: https://github.com/photoprism/photoprism/blob/develop/assets/static/img/preview.jpg"
  style: normal
---

For quite a while I've been looking for a self-hosted photo & video gallery.  
I tried things like:

* [NextCloud](https://nextcloud.com)
* [OwnCloud](https://owncloud.com)
* [Piwigo](https://piwigo.org)
* [Lychee](https://lychee.electerious.com)

Yet, none of them made the cut.

Then, I came across this [Ask HN: Alternatives to Google Photos?](https://news.ycombinator.com/item?id=27338008) thread on Hacker News.
I checked out self-hosted projects mentioned in [this comment](https://news.ycombinator.com/item?id=27339572).

[Photoprism](https://photoprism.app) got my attention as it offers automatic image classification based on Google TensorFlow.
I gave it a spin by following [Getting started instructions for Docker Compose](https://docs.photoprism.org/getting-started/docker-compose/). 
Shortly after I found a [FreeBSD port by Ju Huo](https://github.com/huo-ju/photoprism-freebsd-port).

Since, I'm not a FreeBSD veteran I followed [pinsyd instructions](https://www.truenas.com/community/threads/how-to-install-photoprism-in-jail.88862/post-642024) on how to install Photoprism in TrueNas 12 jail.

These instructions are great, although, I had to make 3 changes.

## 1. Change UID & GID

After pulling [photoprism-freebsd-port](https://github.com/huo-ju/photoprism-freebsd-port) repo,
I've changed `UID` & `GID` in `~/photoprism-freebsd-port/files/pkg-install.in` to `1001`.  
This was to match them with the account I use to manage my photos.

## 2. Apply patch #1

When I ran `make config-recursive && make install`, I got a "duplicate zlib symbol" error:

```log
bazel-out/freebsd-opt/bin/external/com_google_protobuf/src: warning: directory does not exist.
ERROR: /root/photoprism-freebsd-port/work/photoprism-b1856b9d45502ba1a35e1d2ae6ca12fd17223895/docker/tensorflow/tensorflow-1.15.2/tensorflow/BUILD:563:1: Linking of rule '//tensorflow:libtensorflow_framework.so.1.15.2' failed (Exit 1)
ld: error: duplicate symbol: adler32
>>> defined at adler32.c
>>>            adler32.pic.o:(adler32) in archive bazel-out/host/bin/external/zlib/libzlib.pic.a
>>> defined at adler32.c
>>>            adler32.pic.o:(.text.adler32+0x0) in archive bazel-out/host/bin/external/zlib_archive/libzlib.pic.a
...
```

After a bit of reading I've manually applied [following patch](https://github.com/tensorflow/tensorflow/commit/508f76b1d9925304cedd56d51480ec380636cb82#diff-bc2b58339883ae848d484471d86dc99189a40a83ae65ce675a5e636c6b876d4a)
to `~/photoprism-freebsd-port/work/.bazel/dc2e79cdf405c755f2f8c97eebbe740f/external/com_google_protobuf/BUILD`

Basically, I've changed:

```make
ZLIB_DEPS = ["@zlib//:zlib"]
```

to:

```make
ZLIB_DEPS = ["@zlib_archive//:zlib"]
```

and

```make
cc_library(
    name = "protobuf_headers",
    hdrs = glob(["src/**/*.h""]),
    includes = ["src/"],
    visibility = ["//visibility:public"],
)
```

to:

```make
cc_library(
    name = "protobuf_headers",
    hdrs = glob(["src/**/*.h", "src/**/*.inc"]),
    includes = ["src/"],
    visibility = ["//visibility:public"],
)
```

## 3. Apply patch #2

Then, I've applied a second patch described in [this tensoflow issue](https://github.com/tensorflow/tensorflow/issues/31196#issue-475147706).

The `repo.bzl` file was located `~/photoprism-freebsd-port/work/photoprism-b1856b9d45502ba1a35e1d2ae6ca12fd17223895/docker/tensorflow/tensorflow-1.15.2/third_party/repo.bzl`

I've replaced:

```make
def _apply_patch(ctx, patch_file):
    if _is_windows(ctx):
        patch_command = ["patch", "-p1", "-d", ctx.path("."), "-i", ctx.path(patch_file)]
    else:
        patch_command = ["git", "apply", "-v", ctx.path(patch_file)]
    cmd = _wrap_bash_cmd(ctx, patch_command)
```

with:

```make
def _apply_patch(ctx, patch_file):
    if not _is_windows(ctx) and not ctx.which("patch"):
        fail("patch command is not found, please install it")
    cmd = _wrap_bash_cmd(
        ctx,
        ["patch", "-p1", "-d", ctx.path("."), "-i", ctx.path(patch_file)],
    )
```

## Success 🎉

Once patching was done, I re-ran `make install` and after a looooong while the build finished successfully.  
I had further issues with finishing off the installation.

