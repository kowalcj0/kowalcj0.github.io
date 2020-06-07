---
draft: false
title: "Add Basic Auth to Pa11y"
description: "Add Basic Auth to Pa11y"
date: 2020-06-02T16:33:26+01:00
slug: "add-basic-auth-to-pa11y"
toc: false
categories:
  - testing
tags:
  - accessibility
  - nodejs
  - pa11y
cover:
  image: ../pa11y-logo.svg
  caption: "Official Pa11y logo https://pa11y.org/resources/brand/logo.svg"
  style: normal
---
[Pa11y](https://pa11y.org/) is a great open sourced automated accessibility testing tool.  
It uses headless Chrome browser and [HTML_CodeSniffer](http://squizlabs.github.com/HTML_CodeSniffer/) as test runner.

Unfortunately out of the box [Pa11y Dashboard](https://github.com/pa11y/pa11y-dashboard) doesn't come with any form of authentication.
This might be OK for some people, but in our case we're going to add basic-auth to it.

This short tutorial is based on pa11y-dashboard v3.1.0.

## Enter http-auth

I've selected [http-auth](https://www.npmjs.com/package/http-auth) package to do the job as it's a popular and actively maintained package.  
Since v4.0.0 (Feb 2020) the "`Connect integration with http-auth module`" 
(a.k.a. `connect middleware`) was [moved to a separate module](https://github.com/http-auth/http-auth/issues/98).  
It means that we have to also include [http-auth-connect](https://www.npmjs.com/package/http-auth-connect) in our project.


## Dependencies

First things first. Pa11y Dashboard requires [MongoDB](https://www.mongodb.com/) to store task data & test results.  
Spin it up with docker:
```bash
docker run -d --name pa11y-mongo -p 27017:27017 mongo:4.2.6
```

The next step is to add new dependencies to `package.json`:

```diff
--- a/package.json
+++ b/package.json
@@ -30,6 +30,9 @@
     "compression": "~1.7.4",
     "express-hbs": "~2.1.2",
     "express": "~4.17.1",
+    "http-auth": "^4.1.2",
+    "http-auth-connect": "^1.0.4",
     "http-headers": "~3.0.2",
     "moment": "~2.24.0",
     "pa11y-webservice-client-node": "~2.0.0",
```

The last steps in this section is to install project dependencies with:
```bash
npm install
```


## Configuration

Once we're done with dependencies, we have to have a way to specify authentication credentials.  
Let's do that using environment variables. These can be easily defined in `config.js`:

```diff
--- a/config.js
+++ b/config.js
@@ -28,12 +28,19 @@ if (fs.existsSync(jsonPath)) {
       port: Number(env('PORT', '4000')),
       noindex: env('NOINDEX', 'true') === 'true',
       readonly: env('READONLY', 'false') === 'true',
+      username: env('USERNAME', null),
+      password: env('PASSWORD', null),
```


## Changes, changes, changes...

Finally we have to inialize http-auth modules and plug them in to Pa11y app.

```diff
--- a/app.js
+++ b/app.js
@@ -23,12 +23,28 @@ const hbs = require('express-hbs');
 const http = require('http');
 const pkg = require('./package.json');

+// Import http-auth modules
+const auth = require('http-auth');
+const authConnect = require('http-auth-connect');
+
 module.exports = initApp;

 // Initialise the application
 function initApp(config, callback) {
        config = defaultConfig(config);

+    // Configure basic auth
+    const basic = auth.basic({
+            realm: "Visible user area"
+        }, (username, password, callback) => {
+            // Custom authentication
+            // Use callback(error) if you want to throw async error.
+            callback(username === config.username && password === config.password);
+        }
+    );
+
        let webserviceUrl = config.webservice;
        if (typeof webserviceUrl === 'object') {
                webserviceUrl = `http://${webserviceUrl.host}:${webserviceUrl.port}/`;
@@ -54,6 +70,13 @@ function initApp(config, callback) {
                extended: true
        }));

+    // Add authentication module to Pa11y app.
+    app.express.use(authConnect(basic));
+
```


## Start the service

We're now ready to roll!  
Start the dashboard with:

```bash
PORT=8888 USERNAME=a PASSWORD=a node index.js

Pa11y Dashboard started
mode: undefined
uri:  http://:::8888
Server running at: http://0.0.0.0:3000

Pa11y Webservice started
mode:     undefined
uri:      http://0.0.0.0:3000
database: mongodb://localhost/pa11y-webservice
cron:     0 30 0 * * *
```

Then visit [http://127.0.0.1:8888](http://127.0.0.1:8888) enter your username
and password and start using Pa11y 💪😁!

{{< videoloop src="../pa11y-basic-auth.mp4" >}}

