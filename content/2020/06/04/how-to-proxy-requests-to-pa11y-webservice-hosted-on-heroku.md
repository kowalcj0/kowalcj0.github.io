---
title: "How to Proxy Requests to Pa11y Webservice Hosted on Heroku"
description: "How to Proxy Requests to Pa11y Webservice Hosted on Heroku"
date: 2020-06-04T13:39:45+01:00
draft: false
slug: "how-to-proxy-requests-to-pa11y-webservice-hosted-on-heroku"
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
  style: narrow
---

Pa11y-Dashboard runs of top of [Pa11y Webservice](https://github.com/pa11y/pa11y-webservice) (WS).  
By default Pa11y WS listens on port 3000 and Pa11y Dashboard listens on port 4000.  
Unfortunately Heroku doesn't allow its users to easily expose multiple ports per application. 

To overcome this limitation, I've decided to make Pa11y-Dashboard proxy requests to WS via `/ws/` endpoint.

After a bit of searching I've found a dedicated proxy module for expressjs called [express-http-proxy](https://www.npmjs.com/package/express-http-proxy).  

Integration is really simple as it's literally 2 lines of code:

```diff
@@ -23,12 +23,28 @@ const hbs = require('express-hbs');
 const http = require('http');
 const pkg = require('./package.json');
+
+// Initialize proxy module
+const proxy = require('express-http-proxy');
+
 module.exports = initApp;
 
        let webserviceUrl = config.webservice;
        if (typeof webserviceUrl === 'object') {
                webserviceUrl = `http://${webserviceUrl.host}:${webserviceUrl.port}/`;
@@ -54,6 +70,13 @@ function initApp(config, callback) {
                extended: true
        }));
+
+       // Proxy requests to WebService
+       // It will use the same basic auth credentials as all other endpoints
+       app.express.use('/ws/', proxy(webserviceUrl));
```

Once the change is deployed to Heroku you will be able to access Pa11y Webservice 
via `/ws/` endpoint, e.g.:

```bash
curl --user a your-pa11y-app.herokuapp.com/ws/tasks?lastres=true
```

PS. If you followed my earlier [tutorial on adding basic-auth to Pa11y]({{< ref "/2020/06/03/run-pa11y-on-heroku" >}}), 
then you should know that basic-auth will be also added to `/ws/` endpoint.

