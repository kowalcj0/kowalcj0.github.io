---
title: "Run Pa11y Dashboard on Heroku"
description: "configure puppeteer buildpack"
date: 2020-06-03T19:57:26+01:00
draft: false
slug: "run-pa11y-on-heroku"
toc: false
categories:
  - testing
tags:
  - accessibility
  - heroku
  - nodejs
  - pa11y
cover:
  image: ../pa11y-logo.svg
  caption: "Official Pa11y logo https://pa11y.org/resources/brand/logo.svg"
  style: normal
---

To run Pa11y Dashboard on Heroku, you'll need to:
1. add [puppeteer buildpack](https://github.com/jontewks/puppeteer-heroku-buildpack) to your dyno
2. pass `--no-sandbox` argument to Chrome

Puppeteer buildpack will install Chrome and all dependencies required to run it
in headless mode. 

Second step is only necessary if you're going to see following error when
running Pa11y tests on Heroku:

```error
Failed to launch chrome!  No usable sandbox!
Update your kernel or see https://chromium.googlesource.com/chromium/src/+/master/docs/linux_suid_sandbox_development.md
for more information on developing with the SUID sandbox.
If you want to live dangerously and need an immediate workaround, you can try using --no-sandbox.
```

We like to live dangerously so let's use that argument in `config.js`:

```diff
--- a/config.js
+++ b/config.js
@@ -35,7 +35,12 @@ if (fs.existsSync(jsonPath)) {
           database: env('WEBSERVICE_DATABASE', 'mongodb://localhost/pa11y-webservice'),
           host: env('WEBSERVICE_HOST', '0.0.0.0'),
           port: Number(env('WEBSERVICE_PORT', '3000')),
-          cron: env('WEBSERVICE_CRON', false)
+          cron: env('WEBSERVICE_CRON', false),
+          chromeLaunchConfig: {
+                  "args": [
+                          "--no-sandbox"
+                  ]
+          }
   })
```

Once redeployed, your tests should work without any problems.

PS. If you'd like to learn more about "No usable sandbox!" error, please have a look at:

* https://github.com/pa11y/pa11y/issues/411
* https://github.com/pa11y/pa11y#chromelaunchconfig-object

