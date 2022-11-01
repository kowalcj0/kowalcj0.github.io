---
title: "Asorted Django tips and handy links"
description: "Asorted Django tips and handy links"
date: 2022-09-27T15:46:52+01:00
draft: false
toc: true
slug: "django_tips"
categories:
  - programming
tags:
  - django
  - python
cover:
  image: ../django.jpg
  caption: "SRC: [https://linevi.ch/en/category/django.html](https://linevi.ch/en/category/django.html)"
  style: normal
---


## Handy links

* [Django Packages](https://djangopackages.org) - Is a directory of reusable apps, sites, tools, and more for your Django projects.
* [Awesome Django](https://awesomedjango.org) - A curated list of awesome things related to Django. Maintained by William Vincent and Jeff Triplett.


## Show SQL for DB migration

If one of the migrations is running slow, times out or simply affects performance of your DB, 
then you might need to check what kind of SQL statements are actually generated by Django.  

To show underlying SQL, run this built-in command:

```shell
$ pyton manage.py sqlmigrate resources 0001_migration_name_without_dot_py_extention
--
-- Alter field entry on logs
SET log_event_date = true;
ALTER TABLE "logs" ALTER COLUMN "raw" TYPE jsonb;
```
