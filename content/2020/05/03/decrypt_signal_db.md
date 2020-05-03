---
draft: false
title: "Decrypt Signal message DB"
description: "Decrypt Signal message DB & conver it to a valid JSON"
date: 2020-05-03T21:46:49+01:00
slug: "decrypt-signal-message-db"
categories:
  - security
tags:
  - signal
  - sqlie
  - sqlcipher
---

All but the last step are based on this answer on unix.stackexchange: 
https://unix.stackexchange.com/questions/505008/signal-desktop-how-to-export-messages


## Locate db.sqlite & db key

Find Signal DB one of these locations:

* ~/.config/Signal/sql/db.sqlite
* ~/.var/app/org.signal.Signal/config/Signal/sql/db.sqlite


The decryption key is in `config.json` which is located in one thes location:

* ~/.config/Signal/config.json
* ~/.var/app/org.signal.Signal/config/Signal/config.json


## Compile sqlcipher

As of writing, you'll need sqlcipher v3.30 or newer to decrypt Signal's message DB.

Get it from https://github.com/sqlcipher/sqlcipher

Then compile it with dynamic linking:
```bash
./configure \
    --enable-tempstore=yes \
    CFLAGS="-DSQLITE_HAS_CODEC" \
    LDFLAGS="-lcrypto"
make
```

## Decrypt db.sqlite

```bash
/path/to/sqlcipher \
    -list \
    -noheader \
    "db.sqlite" \
    "PRAGMA key = \"x'"${SIGNAL_KEY}"'\";select json from messages;" > clear_text_msgs;
```


## Turn it into a valid JSON file

The file with clear text messages is not a valid JSON, thus we need to:

1. Remove first line, that contains word "ok"
2. Add a comma at the end of every line
3. Add leading `[`
4. Add trailing `]`

```bash
tail -n +2 clear_text_msgs > without_ok
sed '$!s/$/,/' without_ok > with_commas
sed '1 s/^/[\n/' with_commas > with_leading_bracket
echo "]" >> with_leading_bracket
rm without_ok
rm with_commas
mv with_leading_bracket valid.json
```
