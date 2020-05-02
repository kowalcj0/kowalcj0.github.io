---
title: Run your Selenium driven tests in parallel using TestNG.
description: 
date: 2014-03-28T20:47:02
slug: run-your-selenium-driven-tests-in-parallel-using-testng
draft: false
categories:
  - wordpress
  - testing
tags:
  - java
  - selenium
  - testng
---


Sometime ago, I came across this post: [Parallel WebDriver executions using TestNG](https://rationaleemotions.wordpress.com/2013/07/31/parallel-webdriver-executions-using-testng/). 

I thought it'd be good to have it in a repo to save you time setting up your own project. 
Basically this example project runs JUnit tests in parallel using TestNG. 
Tests are grouped by the browser in which they're going to be executed (have a look at the TestNG XML Suite files in `src/test/resources`). 
As you might have guessed to drive the browsers we use Selenium WebDriver :) 
And of course you can run your tests locally or remotely using Selenium GRID. 

You can find the repo on [github](https://github.com/kowalcj0/parallel-selenium-with-testng).

Here's a video showing this project in action :) 
{{< yt id="x1ethgV5gyQ" >}}

