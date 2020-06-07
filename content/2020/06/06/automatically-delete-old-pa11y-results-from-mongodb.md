---
title: "Automatically Delete Old Pa11y Results From MongoDB"
description: ""
date: 2020-06-06T22:56:03+01:00
draft: false
slug: "automatically-delete-old-pa11y-results-from-mongodb"
toc: false
categories:
  - testing
tags:
  - accessibility
  - heroku
  - mongodb
  - pa11y
cover:
  image: ../MongoDB-logo.svg
  caption: "SRC Wikipedia https://upload.wikimedia.org/wikipedia/en/4/45/MongoDB-Logo.svg"
  style: wide
---
You've probably already noticed that Pa11y-Dashboard runs all the tasks on a daily basis. 
If you have a lot of tasks (e.g. 100+) then the test results can fairly quickly gobble up your MongoDB
quota (if you have any).

If your MongoDB has a size limit defined, then you can do two things:
* manually delete old test results
* or use `TTL Index` to do it for you automagically

MongoDB supports [TTL indexes](https://docs.mongodb.com/manual/tutorial/expire-data/) since v2.2 (Aug 2012!). 
Such indexes make `mongod` automatically remove data after a specified number of seconds or at a specific clock time.
Before we create one, please have a look at existing indexes for `Pa11y` test results collection:

```mongodb
db.results.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "heroku_abcdefgh.results"
    },
    {
        "v" : 2,
        "key" : {
            "date" : 1
        },
        "name" : "date_1",
        "ns" : "heroku_abcdefgh.results"
    }
]
```
There should be two indexes. We're interested in the `date_1` index.
We have to remove it before we can add a TTL Index:

```mongodb
db.results.dropIndex({"date": 1});
```

In my case I wanted to keep tests results for the last 31 days.  
So TTL value (`expireAfterSeconds`) should be set to `2678400` (`60*60*24*31`).

```mongodb
db.results.createIndex({"date": 1}, {expireAfterSeconds: 2678400});
```

Let's have a look at the indexes:

```mongodb
db.results.getIndexes()
[
    {
        "v" : 2,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "heroku_abcdefgh.results"
    },
    {
        "v" : 2,
        "key" : {
            "date" : 1
        },
        "name" : "date_1",
        "ns" : "heroku_abcdefgh.results",
        "expireAfterSeconds" : 2678400
    }
]
```

LGTM!

Now, we have to wait a month before we can check if it works as expected ;)


### Backing up the task

Remember to back-up your Pa11y tasks (and results) before every major upgrade or DB operation.  
It takes few seconds to do it and it can save you a lot of time and stress.

```bash
mongoexport \
    --uri=mongodb://username:password@host:61620/heroku_abcdefgh \
    -c tasks \
    -o tasks.json
```

