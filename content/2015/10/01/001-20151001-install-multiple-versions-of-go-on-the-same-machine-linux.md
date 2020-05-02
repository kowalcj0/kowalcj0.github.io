---
draft: false
title: "How to install multiple versions of GO on the same machine [linux]"
description: 
date: 2015-10-01T15:19:01
slug: install-multiple-versions-of-go-on-the-same-machine-linux
---

This quick tutorial shows how to do install multiple versions of go manually. 
I'll try to prepare a shell script that will do it automatically for you :) 

### 1. download different versions of GO

```bash
wget https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz 
wget https://storage.googleapis.com/golang/go1.4.3.linux-amd64.tar.gz 
wget https://storage.googleapis.com/golang/go1.5.linux-amd64.tar.gz 
wget https://storage.googleapis.com/golang/go1.5.1.linux-amd64.tar.gz 
```

### 2. Create directories for specific version of GO

```bash
sudo mkdir -p /usr/local/go/1.4.2/ 
sudo mkdir -p /usr/local/go/1.4.3/ 
sudo mkdir -p /usr/local/go/1.5/ 
sudo mkdir -p /usr/local/go/1.5.1/ 
```

### 3. Unpack downloaded GO releases

```bash
sudo tar -C /usr/local/go/1.4.2/ --strip-components=1 -xzf go1.4.2.linux-amd64.tar.gz 
sudo tar -C /usr/local/go/1.4.3/ --strip-components=1 -xzf go1.4.3.linux-amd64.tar.gz 
sudo tar -C /usr/local/go/1.5/ --strip-components=1 -xzf go1.5.linux-amd64.tar.gz 
sudo tar -C /usr/local/go/1.5.1/ --strip-components=1 -xzf go1.5.1.linux-amd64.tar.gz 
```

### 4. Install `go` alternatives

```bash
sudo update-alternatives --install /usr/bin/go go /usr/local/go/1.4.2/bin/go 2 
sudo update-alternatives --install /usr/bin/go go /usr/local/go/1.4.3/bin/go 3 
sudo update-alternatives --install /usr/bin/go go /usr/local/go/1.5/bin/go 4 
sudo update-alternatives --install /usr/bin/go go /usr/local/go/1.5.1/bin/go 5 
```

### 5. Install `godoc` alternatives

```bash
sudo update-alternatives --install /usr/bin/godoc godoc /usr/local/go/1.4.2/bin/godoc 2 
sudo update-alternatives --install /usr/bin/godoc godoc /usr/local/go/1.4.3/bin/godoc 3 
sudo update-alternatives --install /usr/bin/godoc godoc /usr/local/go/1.5/bin/godoc 4 
sudo update-alternatives --install /usr/bin/godoc godoc /usr/local/go/1.5.1/bin/godoc 5 
```

### 6. Install `gofmt` alternatives

```bash
sudo update-alternatives --install /usr/bin/gofmt gofmt /usr/local/go/1.4.2/bin/gofmt 2 
sudo update-alternatives --install /usr/bin/gofmt gofmt /usr/local/go/1.4.3/bin/gofmt 3 
sudo update-alternatives --install /usr/bin/gofmt gofmt /usr/local/go/1.5/bin/gofmt 4 
sudo update-alternatives --install /usr/bin/gofmt gofmt /usr/local/go/1.5.1/bin/gofmt 5 
```

### 7. Configure version of go, godoc & gofmt interactively

If you want to configure version of go, godoc & gofmt interactively then use: 

```bash
sudo update-alternatives --config go sudo update-alternatives --config godoc 
sudo update-alternatives --config gofmt 
```

### 8. Alternatively you can configure it in a non-interactive way

If you want to configure version non-interactively then use: 

```bash
sudo update-alternatives --set go /usr/local/go/1.4.2/bin/go 
sudo update-alternatives --set godoc /usr/local/go/1.4.2/bin/godoc 
sudo update-alternatives --set gofmt /usr/local/go/1.4.2/bin/gofmt 
sudo update-alternatives --set go /usr/local/go/1.4.3/bin/go 
sudo update-alternatives --set godoc /usr/local/go/1.4.3/bin/godoc 
sudo update-alternatives --set gofmt /usr/local/go/1.4.3/bin/gofmt 
sudo update-alternatives --set go /usr/local/go/1.5/bin/go 
sudo update-alternatives --set godoc /usr/local/go/1.5/bin/godoc 
sudo update-alternatives --set gofmt /usr/local/go/1.5/bin/gofmt 
sudo update-alternatives --set go /usr/local/go/1.5.1/bin/go 
sudo update-alternatives --set godoc /usr/local/go/1.5.1/bin/godoc 
sudo update-alternatives --set gofmt /usr/local/go/1.5.1/bin/gofmt 
```

### 9. Set the GOROOT env variable to match the location of selected version of GO

set `GOROOT` to your current version of GO 

```bash
export GOROOT=$(dirname $(dirname $(readlink -f $(which go | cut -d" " -f3))))
```

