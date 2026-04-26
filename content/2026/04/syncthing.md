---
title: "Hosting Syncthing services"
description: "Hosting your onw instances of Syncthing discovery and relay services"
date: 2026-04-26T23:38:07+01:00
draft: false
toc: false
slug: "syncthing-services"
categories:
  - unix
tags:
  - linux
  - docker
  - syncthing
cover:
  image: https://syncthing.net/img/logo-horizontal.svg
  caption: ""
  style: normal
---


I used [syncthing-relay-discovery](https://github.com/t4skforce/syncthing-relay-discovery) by `t4skforce` for quite a while, but recently I found out that Syncthing Team publishes their own images for [Relay](https://hub.docker.com/r/syncthing/relaysrv) and [Discovery](https://hub.docker.com/r/syncthing/discosrv/) services.
In comparison to the t4skforces's image, the new ones combined are half the size:

```shell
$ docker images -a
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
syncthing/discosrv   2.0.16    e06d667325fa   2 weeks ago     28.7MB
syncthing/relaysrv   2.0.16    1398765edf65   2 weeks ago     22.4MB
```

So, without much ado, I created a `docker-compose.yaml` and reused my existing certificates:

```yaml
services:
  relaysrv:
    image: syncthing/relaysrv:2.0.16
    container_name: sync-relay
    restart: always
    ports:
      - "22067:22067"  # Relay data port
      #- "22070:22070"  # Status/statistics port
    volumes:
      - ./certs/cert.pem:/var/strelaysrv/cert.pem
      - ./certs/key.pem:/var/strelaysrv/key.pem
    environment:
      - PUID=1000
      - PGID=1000
    command: ["-pools="]

  discosrv:
    image: syncthing/discosrv:2.0.16
    container_name: sync-disco
    restart: always
    ports:
      - "8443:8443"    # Discovery protocol port
      #- "19200:19200"  # Status/metrics port
    volumes:
      - ./certs/cert.pem:/var/stdiscosrv/cert.pem
      - ./certs/key.pem:/var/stdiscosrv/key.pem
      - ./discosrv-data/records.db:/var/stdiscosrv/records.db
    environment:
      - PUID=1000
      - PGID=1000
```
