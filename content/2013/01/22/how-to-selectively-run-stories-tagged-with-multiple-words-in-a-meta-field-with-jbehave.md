---
title: How to selectively run stories tagged with multiple words in a meta field with jBehave
description: 
date: 2013-01-22T17:17:29
slug: how-to-selectively-run-stories-tagged-with-multiple-words-in-a-meta-field-with-jbehave
draft: false
categories:
  - wordpress
  - testing
tags:
  - java
  - jbehvae
  - bdd
  - mvn
  - gherkin
---

## Prerequisites

1) a working jBehave based project 

This short tutorial is based on an jbehave-tutorial project available on github: 
<https://github.com/jbehave/jbehave-tutorial>. 

To be precise I used the `java-spring` submodule from the `etsy-selenium` module, 
available here: <https://github.com/jbehave/jbehave-tutorial/tree/master/etsy-selenium/java-spring>, 
to run the modified story presented below. 

2) Maven

OK, let's consider a situation when we have stories belonging to multiple features, categories etc.  
Below is an example story, tagged with multiple categories and features: `anExampleStoryWithMultipleWordsInAMetaKeyword.story` 

```
Meta: @categories category1 category2 category3
@features feature1 feature2 feature3 feature_4 
Scenario: scenario description Given I'm on the homepage ....
```

Now, we'd like to run stories only for a selected category or a feature. 
To accomplish this we'll use the value pattern matching mechanism implemented 
in the jBehave meta matcher and described on [jBehave Meta Matchers](https://jbehave.org/reference/stable/meta-filtering.html) reference page.

## Usage examples

Run stories covering only `category3`:
```bash
mvn clean install -Dmeta.filter="+categories *category3*"
```

Run stories covering only `feature_4`:
```bash
mvn clean install -Dmeta.filter="+features *feature_4*"
```

And finally, run stories matching `feature2` and `category1`:
```bash
mvn clean install -Dmeta.filter="+features *feature2* +categories *category1*"
```


## Notice

It seems that jBehave is not handling `-` hyphens in the keyword value properly, 
but it works fine with `_` underscores, separate words and camelCase notation :)

