---
draft: true
title: "import zipfile"
description: "A brief overview of various CLI tools that can help you diagnose your FreeBSD system"
slug: "import-zipfile"
date: "2020-03-30T20:05:24+01:00"
toc: true
categories:
  - programming
tags:
  - python
  - zip
---

Recently, I had a look at [zipfile](https://docs.python.org/3/library/zipfile.html) module.  
It's surprisingly easy to work with.  
Snippets below should give you a rough idea how to use it.


## Create a zip file

```python
import zipfile

file_to_compress = "server.log"
zip_file_name = "server.log.zip"

with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as myzip:
    myzip.write(file_to_compress)
```

NOTE: 3rd argument defines the compression type.

Choose from:

* ZIP_STORED (no compression)
* ZIP_DEFLATED (requires zlib)
* ZIP_BZIP2 (requires bz2)
* ZIP_LZMA (requires lzma)


### Unpack a zip archive

```python
with zipfile.ZipFile(zip_file_name, "r") as myzip:
    myzip.extractall()
```

### List zip file details & test the archive

```python
with zipfile.ZipFile(zip_file_name, "r") as myzip:
    # list archive details
    print(myzip.infolist()) 
    
    # list all file inside the zip file
    print(myzip.namelist())
    
    # Read all the files in the archive and check their CRC’s and file headers. 
    # Return the name of the first bad file, or else return None.
    assert myzip.testzip() is None
```


## Create a password protected zip file

```python
import zipfile

protected_zip_file_name = "server.log.pass.zip"
file_to_compress = "server.log"
pwd = "password"

with zipfile.ZipFile(protected_zip_file_name, "w", zipfile.ZIP_DEFLATED) as myzip:
    myzip.setpassword(pwd = bytes(pwd, "utf-8"))
    myzip.write(file_to_compress)
```


### Unpack password protected zip file

```python
with zipfile.ZipFile(protected_zip_file_name, "r") as myzip:
    file.extractall(pwd = bytes(pwd, "utf-8"))
```


## Hashes & Checksums

### Calculate CRC

```python
import zlib

with open(zip_file_name, "rb") as in_file:
    print(zlib.crc32(in_file.read()))
```


### Calculate MD5

```python
import hashlib

hash_md5 = hashlib.md5()

with open(zip_file_name, "rb") as in_file:
    for chunk in iter(lambda: in_file.read(4096), b""):
        hash_md5.update(chunk)
    print(hash_md5.hexdigest())
```
