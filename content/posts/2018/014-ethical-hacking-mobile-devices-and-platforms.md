---
draft: false
title: "Ethical Hacking - Mobile Devices and Platforms - notes"
description: "Notes from a video course"
slug: "ethical-hacking-mobile-devices-and-platforms"
date: "2018-04-28T10:29:15+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
  - mobile
  - android
  - iOS

featuredImage: /img/2018/004/ethical-hacking-wikimedia.jpg
featuredImageDescription: "Source: [wikimedia.org](https://commons.wikimedia.org/wiki/File:Ethical-hacking.jpg)"
dropCap: false
---

Good sources of knowledge:

* OWASP Testing guide - book
* OWASP Pinning cheat sheet


# Android Application

* Executes as:
    * application
    * service
* Helpers
    * Broadcast receiver (allows app to register for specifi events which will
        be then passed to it for action)
    * content provider (it interfaces between app and file storage and provide
        sql-like interface to read/write/modify/delete data). `SQLite` is a
        common DB service access via content provider.


## Android Intents

* these are objects used to manage requests. They include action and relevant
    data for the request being made. It can be used to:
    * start an activity
    * access broadcast receiver
    * start a service
* App can register to listen for an intent activity request by including it in
    app's `manifest` file
* An `Intent` can explicitely define it's target application or let the system
    identify application or applications able to respond. If ther's more than
    one, the Android will display an application picker.
* Applications can export activities as `application-application intents`
* Apps can also access broadcast receivers & content providers exported by
    other applications. 
* Intents are also used for inter-process communication
* Intent usage:
    * startActivity - may include & return data. Usuall one per app screen
    * startService
    * sendBroadcast - a msg sent using one of three send broadcast intents
* Intents can be explicit (sent to an app or component) or implicit (OS find
    appropriate recipient of the msg)


## Android Security Model

* The trust boundary is the application not the user (just like on Linux)
* Apps run it their own sandbox
* Interactions are explicit
* Apps are signed
* Application must have a valid certificate
    * self-signed
    * authority-signed
* Unfortunatelly Android does not do cert chain validation
* In Android 6 busybox was replaced with toybox


## Sandboxing applications

* each app has it's own unique ID
* it runs in its own Sandbox
    * which cannot interfere with other apps
    * and other apps cannot interfere with it
* its data (files) are stored in the sandbox
* shared files are shared via content providers
    * you can use content providers for app only data but you'll have to mark 
        it as `not-exported`
* keystores can be used to protect data by prompting user for the password to
    access it.


## Android permissions

* apps has to explicitly request permissions to access camera, clipboard etc
* the good practice is to minimise permissions requested
* apps can use standard permissions or define they're own
* permissions are groupped in two protection levels: normal or dangerous (which
    requires explicit user consent)
* app declares required permissions in its manifest file.


# apk tools

* APK Tool - Handy tool to analyse APKs.  Download it from [https://ibotpeaches.github.io/Apktool/install ](https://ibotpeaches.github.io/Apktool/install).
* [dex2jar](https://sourceforge.net/dex2jar)
* [JD-GUI](jd.benow.ca) - java decompiler
* fortify - paid tool
* [Android-x86](www.android-x86.org) run android in regular VM
* [the bouncy castle](https://www.bouncycastle.org) - is a lightweight Java
    crypto lib
* [JAD - Java Decompiler](vareneckas.com/jad/)
    * once you converted dex files to java files, then
    * `jad -d outputdir -s java dirwithjavafiles/*.*`
* [jadx](https://sourceforge.net/jadx) - Dex to Java decompiler
* github/android-security-awesome - list of handy android security tools
    * [drozer](https://labs.mwrinfosecurity.com/tools/drozer/) - it needs an
        `agent` app to be pushed to the test device.


# Drozer

[drozer](https://labs.mwrinfosecurity.com/tools/drozer/) - it needs an `agent`
app to be pushed to the test device.

```shell
adb install agent.apk   # install drozer agent
adb forward tcp:31415 tcp:31415  #we have to forward ports for it to work
drozer console devices  # then start the drozer agent on the app
drozer console connect  # connect server to the agent
```

Once you're in the drozer's shell:

```shell
dz> list   # list all available drozer modules (plugins)
dz> run app.package.list  # list all packages (applications) on the devices
dz> run app.package.info -a com.you.app  # app details: perms, uid, gid, ver.
                                         # data & apk location etc
dz> run app.package.attacksurface com.your.app
# shows potential attack surfaces, like:
# number of exported actitivies, broadcast receivers or content providers
# it can also show whether debugging mode is available

dz> run app.activity.info -a com.your.app
# will list all exported app activities and required permissions. If `null`
then you don't need any permission to access it.

dz> run app.activity.start --component com.your.app com.your.app.DeepLinkActivity
# create an intent to access the activity

dz> run app.service.info -a com.your.app  # list exported services

dz> run app.service.send com.your.app com.google.firebase.iid.FirebaseInstanceIdService baaadText 2 3
# if error is produced, then we can analyse the decompiled source code (if 
available) and try other values until we succeed.

```


## common Android files

* `wal` is a temporary write-ahead logging file
* `shm` is an index file for `wal`


# iOS applications

* iOS apps can interact only with directories stored within its sandbox
* during installation iOS generates UUID and creates content directories for
    the app inside the sandbox dirs.
    * `bundle container` - app container named `yourappname.app`. This folder
        is signed, and any changes to it will prevent app from running
    * `data container` - holds runtime data for both the app & the user
        * this directory is further divided into other subfolders, which app
            can use store its data:
            * `Documents` user generated content
            * `Library` internal app data
            * `tmp` used to write temp data during the current app invocation
        * there can be other folders in `data container` which will be app
            specific ones.
    * depending on the iOS version, `bundle` & `data` dirs can be store in the
        same or different location (since iOS 8)
* in `bundle container` there's `Info.plist` - it's a plain xml file which
    contains basic info about app required to run it:
    * name
    * ID
    * main executable
    * etc.


## Areas to test


### Application data storage

There are three main storage options:

* SQLite
* property list files
* keychain

All of those can be used with default security settings, but can be also
configured.


## Stored Data Protection

* All app data is encrypted at rest (using a file system key)
* When devices is turned on, then data is unlocked (decrypted)
* File access permissions:
    * No protection
    * Complete protection - the file in inaccessible when device is locked
    * Complete unless open - the file in accessible if application has it open
        when the device is locked
    * Complete until first user authentication - the file is always accessible
        after the first unlock. (This is the default setting)
* Key Chain - has multiple security options, like:
    * Write only if passcode is set
    * Read on this device only


### Cached and temp data

iOS stores an unencrypted screen shot of the app when it goes to the 
background which can be used to recover any sensitive information that is
visible on that screen.

Request & Response data is stored in SQLite DB called `cached.db`.

### URL handlers

Some apps might use URL handlers to pass sensitive information between
processes (they will be listed in `Info.plist` under `URLTypes` section)


### Binary protection

Many apps uses extra flags to secure the app binary, like: Data Execution
Prevention (`DEP`), `Postion Independent Executable` & `ASLR`.  
It's good to check for those flags.

402

# iOS Security


```text
   --------        ---------------       ---------       ----------
   | Boot |        | Low level   |       | iBoot |       | Kernel |
   | rom  |  -->   | Boot loader |  -->  | load  |  -->  | Load   |
   --------        ---------------       ---------       ----------
```

* `Boot rom hardware` contains `RO` code to bootstrap the system and Apple's
    public key.
* Public key is used to verify the integrity of the `Low level boot loader`
    code
* `Low level boot loader` takes the 2nd stage boot called `iBoot load` code 
    from flash memory and verifies its signature before loading.
* `iBoot load` verifies the Kernel code in similar fashion before loading it.

This process provides a secure way of loading the System.


## Application Sandboxing

* all apps run in sandboxes, but not all apps use all security features
    provided by the iOS
* Interactions outside the sandbox have to be explicit. For example accessing
    microphone, camera, media etc.


## Exploitation protection

* Memory pages can be marked as "Write but not execute" (using ARM chip `W^X`
    feature, similar to `DEP` for Windows users)
* `ASLR` - makes sure that code & data are not stored together, so it makes
    exploitaion of fixed memory addresses more difficult
* `Position-independent execution` (`PIE`) - allows application to work from
    any location in memory
* `Stack canaries` - can be used to check for malicious or accidental stack
    overwrites. A function can always check whether "`canary`" is stil alive.


## Interesting folders on iOS devices

* `/var/stash`
* `/var/mobile`
    * `/var/mobile/Applications` -> contain a bunch of UUIDs sandbox folders 
        for each application
    * `/var/mobile/Containers` -> similar as above.
    * `/var/mobile/Library/Accounts`
        * contains files like `Accounts3.sqlite`
    * `/var/mobile/Library/SMS`
        * contains files like `sms.db` - with all SMS msgs in clear text
    * `/var/mobile/Library/Media` - contains books, photos etc


### iOS testing tools

* Once iOS device is jailbroken and you install `openssh` via `Cydia` you can 
    change root password with `passwd`
* `Erica` - allows to view plist files in human readable mode
    * example usage: `plutil Info.plist`
* [Clutch](https://cydia.iphonecake.com) - identify all encrypted applications
    and reverse engineer them to allos src code analysis. It decrypts an app
    and dumps it into an `ipa` file.
    * `chmod +x /usr/bin/Clutch` - this has to be done before running
    * `Clutch -i` → list all encrypted applications
* [Class-Dump-Z](cydia.radar.org) - 
* IPA Installer
* WinSCP - handy when exchanging files between phone and laptop
* IDA Pro
* [Snoop It](https://www.nesolabs.de) - used for dynamic analysis of 
    application operation. 
* [hopperapp](htpps://www.hopperapp.com) - handy disassembler


## Extracting properties and class headers


```shell
# list all encrypted apps
root# Clutch -i

# decrypt selected app into an ipa file (which essentially is a zip file)
root# Clutch -d 8

# replace installed encrypted app with its decrypted ipa counterpart, this is
# useful cos we can extract properties list and class headers
root# ipainstaller -c yourapp.ipa

# go to the dir below to find all app files
cd /private/var/mobile/Applications/{your_app_UUID}/

# NOTE: remember to not to modify, remove or add files to the app dir folder as
# it will stop working due to folder signature mechanism

# extract properties (manifest file) from Info.plist file
root# plutil Yourapp.app/Info.plist > properties_list

# Extract resource rules
root# plutil Yourapp.app/ResourceRules.plist >> properties_list

# extract class headers with class-dump-z
root# class-dump-z Yourapp.app/Yourapp >> properties_list
```

