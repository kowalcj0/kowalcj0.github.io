---
draft: false
title: "Ethical Hacking - Denial of Service - notes"
description: "Notes from a video course"
slug: "ethical-hacking-denial-of-service-attacks"
date: "2018-04-23T19:19:15+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
  - DoS

featuredImage: /img/2018/004/ethical-hacking-wikimedia.jpg
featuredImageDescription: "Source: [wikimedia.org](https://commons.wikimedia.org/wiki/File:Ethical-hacking.jpg)"
dropCap: false
---

These are just my notes from the Pluralsight course: "Ethical Hacking: Denial 
of Service" by Troy Hunt.


# HTTP flood attack

* HTTP flood attack
    * it's a "volumetric" attack - they're normal HTTP requests
    * it can saturate web server resources ("service request flood")
    * can saturate bandwidth ("bandwidth attack")
* Attack effectives can be amplified via certain app features:
    * They use resources (login page, api endpoint) that takes a lot of
        resources or time to process (like slow hashing function on login page)
    * requests that result in SMTP connections (sending email after registering
        dummy accounts, password reset page etc)
    * long-running requests (like DB heavy requests)
    * download of large files to flood bandwidth
* Requests can adhere to legitimate patterns which makes defence difficult


# TCP attacks

These are the layer 4 (OSI) attacks

TCP handshake:

```text
             SYNchronize
    ----------------------------→

      SYNchronize-ACKnowlegement
SRC ←---------------------------- TRGT

            ACKnowledge
    ----------------------------→
```


## SYN flood attack

```text
             SYNchronize
    ----------------------------→

      SYNchronize-ACKnowlegement
SRC ←---------------------------- TRGT

    SRC does not respond with ACK
```


## SYN flood attack with spoofed source IP address

```text
    SYNchronize (spoofed src IP address)
SRC ----------------------------→

      SYNchronize-ACKnowlegement
3rd ←---------------------------- TRGT
party
```


# UDP and ICMP attacks

* `UDP` (User Datagram Protocol)
    * usually it's a flood of UDP packets send to random ports on the target
    * the target consumes resources responding with "destination unreachable"
        packets
    * No initial handshake means source IP can be spoofed for anonymization
* `ICMP` (Internet Control Message Protocol)
    * Supports utilities such as ping using `echo request` and `echo replay`
    * source IP in a ping can be forged to create a "Smurf" attack
    * can be used to send a "Ping of Death", a large packet causing a buffer
        overlow


# DNS Amplification attack

* sometimes called `DNS Reflection` attack
* attacker sends a smal request for e.g. all DNS records for particular zone
    which generates a large response

```text
           Small spoofed DNS request
Attacker ----------------------------→ DNS Server
                                             Large amplified response
                                          ----------------------------→ Target

```

# Other forms of amplification attack

* `SNMP` (Simple Network Management Protocol)
    * can amplify by a factor of 650x
* `NTP` (Network Time Protocol)
    * can return a large resul via the `monlist` command
    * runs over UDP
    * src IP can be spoofed
    * amplification factor can be up to 206x
* `SSDP` (Simple Service Discovery Protocol)
    * Attacker query home devices with `uPnP` services enabled
    * Responses are larger than the incoming request
    * src IP can be spoofed


# P2P Attacks

* works in `DC++` networks
* uses flaw in the implementation to ask p2p peers to disconnect from the
    network and send requests to external target.


# Slowloris

* "Low and slow" attack tool
    * uses a low volume of trafiic to generate a slow rate
* Sends HTTP requests without a termination sequence
    * Causes website to leave the connection open
    * Resources are allocated to wait for the termination sequence
* Can originate from a single origin
    * Partial requests are sent and then resent and then resent ...

```text
          Uncompleted HTTP GET request
          ----------------------------→
          Uncompleted HTTP GET request
          ----------------------------→
Attacker  Uncompleted HTTP GET request    Target
          ----------------------------→
          Uncompleted HTTP GET request
          ----------------------------→
```


# Permanent DoS and Phlashing

* `PDoS` attack renders a device unusable, usually by replacing firmware
    (flashing)
* also referred to as "`bricking`"
* exploits weaknesses in the target device (e.g. update process)


**Interesting attacks:**

* GitHub's Man on the Side Attack
* Incapsula Client's DDoS attack by botnet called "`Cutwail`"/"`PushDo`"


# Tools

* `LOIC` a C# tool written in 2004, frequently used by `hacktivists`
* `JS LOIC` JS version of Loic
* DoSHTTP - DoS HTTP Flood DoS testing tool
* DoS booters - tools you can rent for performing a DoS
    * eg. top10stressers.com, booter.xyz
* [loader.io](https://loader.io) a legit stress testing tool by SendGrid



# Defence

* do you have multiple defence types depending on the attack?
* are you able to adapt as the attack does?
* Can you do all this without neglecting other security imperatives?


## Discovering the attack pattern

* Is it a lyaer 4 (UDP, TCP, ICMP) or layer 7 (HTTP) attack?
* What's the source and the target
* are there any unique signatures like headers or target resource
* What's the intent? is it definitely malicious or unitentional DDoS caused by
    .e.g. misconfiguration? 


## Absorbing the attack

If your `Capacity > Attack` then:

**Pros:**

* No distruption for legitimate users
* Auto-scale is simplified when using cloud services
* Scaling buys time to determine other countermeasures


**Cons:**

* can be very expensive
* may not be practical withing a short timeframe
* may not practically feasible for a large enough attack


## Establishing Traffic Reputation

* When does normal traffic look like?
    * where do people come from and what do they do?
* How much of a deviation constitute potentially malicious traffic?
* What layers of defence are available when repoutation thresholds are
    exceeded?
* For example:
    * what does a normal login process look like?
    * e.g. if user attempts more than 3 times to login, then present them
        captcha or other challange
    * this won't stop the attack, but will prevent the site from doing a CPU or
        IO sensitive work


# Network Level Defences


* Hardware appliances
    * like first line of defence places before a firewall
    * firewalls
    * `IPS` - Intrusion Prevention System
    * `SLB` - Software Load Balancer
    * `WAF` - Web Application Firewall
* Layer 4 countermeasures
    * Disable all unused ports
    * block unnecessary protocols (i.e. `ICMP`)
    * Filter ingress traffic
        * Repotation bsased blocking
    * Implemented "blackholing" or "tarpitting"
        * Terminate traffic upstream of the origin server
        * No response is sent, the traffic just "disappears"
        * can route traffic to a different segment of network for further
            analysis.
    * This only works if the network isn't saturated with data
* `Anycast`
    * network addressing and routing methodology, in which you can stand up a
        single IP address and then depending on where the traffic originates 
        from route it to the nearest possible node. So from the outside world
        your service is available via only 1 IP address.


# Application level defences

* In case there's not anomalous layer 4 traffic
* but there's a lot of HTTP traffic
* then you can use `WAF` (Web Application Firewall) which can inspect HTTP
    traffic
    * make sure `WAF` can also inspect HTTPS traffic
* Minimize the attack surface area
    * take any resources (admin panels, reporting pages etc) from the publicly
        available network and place then in the private subnet
* Design the application for `DDoS` resiliency by `Sandboxing Application
    Features`
    * run application features (modules) on separate nodes/servers
    * so that when one module is under attack, then only this module is
        unavailable and remaining modules work fine.


# Preparing for DoS Resiliency

* Implement a DoS strategy well in advance of an attack
* Test your defences
* Do you have a crisis management plan (DDoS Runbook)?
    * check "DDoS RunBook" created by Robert Handson of Whitehat security
* Do you know how much a successful DoS attack will cost you?
    * this will justify the costs involved with improving your defence

