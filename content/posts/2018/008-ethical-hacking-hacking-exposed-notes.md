---
draft: false
title: "Ethical Hacking - Hacking Exposed - Notes"
description: "Notes from video course"
slug: "ethical-hackin-hacking-exposed"
date: "2018-02-26T21:20:12+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
cover:
  image: /img/2018/004/ethical-hacking-wikimedia.jpg
  caption: "Source: [wikimedia.org](https://commons.wikimedia.org/wiki/File:Ethical-hacking.jpg)"
  style: normal
---
These are just my notes from the video course: "Ethical Hacking: Hacking
Exposed" by Troy Hunt.


# Intro

Questions to ask and answer when deciding on levels of security:

* What is most confidential to you?
* What can't you afford to lose?
* What is irreplaceable?
* What could cause the most damage?
* What might impact your reputation?

The answers to those question will specify your `security assets` that you will
protect.


# Privacy vs Anonimity

Privacy -> is when someone potentially know who you are, but they don't know
what are you doing or with whom you're talking. It's all about confidential
content.

Anonimity -> is keeping your actions and activities separate from your true 
identity. Non-attribution to your actions.
Anonimity is usally desired when viewing content rather than when creating it.

Pseudonymity -> is when you wish to retain reputation against an identity. 
e.g. a cover, an alias a false identity.

In most countries you have [Right to privacy](https://en.wikipedia.org/wiki/Right_to_privacy).


*Read on:*

* JonDonym


# Risk = Vulnerabilities x Threats x Consequences

The outcome of suitable security processes, actions and technology is the
protection of your assets, privacy and anonimity.


# Threat modelling and Risk Assessments

{{< gallery >}}
{{< figure link="/img/2018/009/The-Cyber-Security-Landscape-Diagram.png" thumb="-thumb" size="1921x1081" caption="The Cyber Security landscape" >}}
{{< /gallery >}}

Source: [Pluralsight](https://www.pluralsight.com)

You never can have 100% security, anonimity etc. There always will be some
risk.

**Security** is:

* a technology
* an action (to mitigate threats & adversaries, to protect assets, privacy &
    anonimity)
* a process

You have to decide what's your tolerance for risk (what consequences you can
bear).
You have to decide where's the balance between:  
* usability and security, between
* risk and opportunity


**You need to:**

* analyse and understand the positive and negative outcomes of security 
    threats or opportunities
* You need to take the risk based approach to apply right level of security
* Consentrate on consequences when threats & adversaries are less tangible to
    discover.


**Layers of security landscape**

1. `Assets` -> what you want to protect
2. `Vulnerabilities` -> bugs, weaknesses in your systems and processes
3. `Threats` -> potential threats posed by Adversaries
4. `Adversaries` -> potential malicious actors
5. `Consequences` -> money/data/privacy/anonimity/reputation loss, data 
    malformation or leakage etc.

Security controls on an example of a stolen laptop with sensitive data being 
stored in plain text:

1. `Select` -> e.g.: whole-disk encryption, boot sector encryption and 
    pre-boot anuthentication
2. `Implement` -> install LUKS whole-disk encryption
3. `Assess` -> check if disk encyption is working and data is accessible
4. `Monitor` -> monitor for LUKS security updates, bugs, vulnerabilities


# Security vs Privacy vs Anonymity

> Privacy isn't about hiding something. It's about being able to control how we
> present ourselves to the world. It's about maintaining a public face while at
> the same time being permitted privated thoughts and actions. It's about
> personal dignity. Bruce Schneier.


# Defence in Depth

```
->          |   ->   |          ->
->  Prevent | Detect | Recover  ->
->          |   ->   |          ->
```

* Prevention - encrypt filkes, and make sure keys & passwords isn't available
    to unauthorised parties
* Detection - set up a `canary`, a delibarate trap, so when it's triggered then
    you're notified that something's wrong
* Recovery -> backup, ablity to recover lost files or other asset


# The zero trust model

Evaluate (tools, services) instead of trusting others.

> e.g.
> Given you'd like to store files on Dropbox, you can encrypt your files before
> uploading them there, and keep the key in a separate safe location.
> This way you distribute the trust to the alternative backup locations.

`Cryptopn` & `Encryptr` are examples of `zero knowledge` services.

# Know Your Enemy

{{< gallery >}}
{{< figure link="/img/2018/009/top-three-thing-you-do-to-stay-safe-online-experts-vs-non-experts.png" thumb="-thumb" size="817x471" caption="Top three thing you do to stay safe online? - experts vs non experts" >}}
{{< /gallery >}}

Source: [Pluralsight](https://www.pluralsight.com)

{{< pswp-init >}}

> Complexity is the enemy of security.

# Types of Malware

Below are strict taxonomies.

* Macro Virus -> malicious code embeded in various documents written in various
    macro languages, like VBS
* Stealth Virus -> one that hides the modifications it made, and fools
    antivirus by intercepting its requests to OS, so that it thinks there's no
    issue.
* Polymorphic Virus -> one that creates various copies of itself, which
    frequently are different from each other and thus it's harder to detect
* Self-garbling -> hide from AntiVirus software by modying tis code
* Bots & Zombies -> hacked devices under a control of a botnet C&C
* Worms -> virus that spread from machine to machine
* Rootkits -> embeded to the OS or bootsector and can hide its existence
    completely
* Firmware Rootkit -> one that resides in your hardware's firmware
* Keyloggers -> log your key strokes
* Trojan horses -> a program that appears and behave as one thing but at the
    same time it's also a malware
* RAT (Remote Access Tool) -> provide back-door access to your system e.g.:
    `Snakerat`
* Ransomware -> usually a malware that encrypts your files, and you usually 
    have to pay some ransom to get the decryption key (or not)
* Malvertisement -> online ad that is infected with virus/malware, frequently
    hidden behind a chain of advenrtisement networks
* Drive-by Attack -> visiting a compromised website which serves you a
    malicious content
* Spyware -> gather information on you and send it to the hackers/criminals
* Adware -> hijacks your default search engine, displays ads in your browser
    (sometimes called as browser-hijacking)
* Scareware -> a type a social engineering attack, which tries to trick user
    into believing into a threat which isn't real, like fake viruses
* PUP (Potentially Unwanted Programs) -> it'a catch-all term for programs that
    you potentially don't want, frequently are bundled in with the software.

# Phishing

Trick a person into clicking on a link or executing malware in some way.
It might be an attempt to compromise device security and open the doors for 
further malicious activity. It's a form of social engineering.

Roughly 30% of poeple get fooled by this kind of attacks.

Spearphining -> a targetted (personalised) phishing attack.

* subdomain & missspelt domains
* IDN homograph attacks
* Hidden URLs
* Left-to-Right tricks


# Spam, Scams & Social engineering

CHECK -> AV Test spam origin map
CHECK -> consumerfraudreporting.org
CHECK -> actionfraud.police.uk/types_of_fraud

* lottery
* fake check payments
* computer performance scans / fix non-existing computer problems
* refund / recovery scams
* scholarship
* online dating scams (claim to need some money in emergency)
* facebook fake friend scams


# Doxing 

* Doxing -> find personal & private information to cause embarassment, discredit,
extort, coerse, harras and cause the problems to the victim.


**Five Eyes:**

1. Australia
2. Canada
3. New Zealnd
4. UK
5. USA

**Nine Eyes:**

6. Denmark
7. France
8. Netherlands
9. Norway

**Fourteen Eyes:**

10. Belgium
11. Germany
12. Italy
13. Spain
14. Sweden

Example programs used by those countries to exchange intelligence data:
Carnival, Echelon, Narrows Inside

Interesting devices:

* retro-reflectors (audio, keyboards, video cables) -> mostly passive devices,
    use almost no power but can reflect signals when they're exposed at
    specific directed signal beam

# Encryption

**Asymetric**:

* Bettery key distribution
* Scalability
* Authentication and nonrepudation
* Slow
* Mathematically intensive


**Symmetric**:

* Fast
* Strong


**SSL != TLS**

* `SSL` -> is older than `TLS`, and has security vulnerabilities.

Read more on TLS on [Wiki](https://en.wikipedia.org/wiki/Transport_Layer_Security)

`TLS 1+` is recommended on server side.

# Cipher suite from Mozilla:

[Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)

[ssl-config-generator](https://mozilla.github.io/server-side-tls/ssl-config-generator/)


**Various Tools:**

* arpwatch
* sniffdet -> a set of tests for remote sniffers detection in TCP/IP networks.
* `ssllabs.com` -> test server ssl config


# End-2-End-Encryption E2EE

* `ZRTP` - Z Real Time Protocol
* `OTR` - Off The Record
* `SSL/TLS`
* `PGP`

**Notes**

* Read article "Security Pitfals in Cryptography" by Bruce Schneier
* have a look at the top 50 products by total number of Disctinct
    Vulnerabilities on cvedetails.com
* Buying into the bias: why vulnerability statistics suck    
* check → tosdr.org for info on privacy statements summaries
* check → eff.org who has you back govenrment data requests
* check → bugmenot.com generate disposable accounts for you
* receive-sms-online.info → disposable sms accounts
* check → parsemail.org
* search for thunderbird plugin that allows to check attachments via virustotal
* prxbx.com/email → a list of email providers grouped by privacy concerns
* spoon.net/browsers → browser sandbox
* bufferzone.com → windows commercial app sandbox
* shadowndefender.com -> windows only sandbox-like tool
* faronics.com `deep freeze` → restores system to given snapshot after reboot
* apparmor → specify what files programms can access
* sandfox → sandbox for linux
* selinux → 
* sandbox → a commnad installed on some systems
* firejail → sanbox
* trustedbsd.org → 
* whonix → a distro that uses Tor to connect to internet
* qubes os
* techmonkeys.co.uk -> check if your router is in the DB of hacked routers
* Qualys FreeScan -> apparently v.good online vulnerability scanner
* adeptus-mechanicus.com -> reports on password hashes etc
* hashcat.net
* crackstation.net -> pay for cracking passwords
* `corskreew` -> tool for tunneling SSH through HTTP proxies
    * `ssh -p 22 -o 'ProxyCommand corkscrew -p 192.168.1.1 <PROXY_PORT> 
        %d %p ' -D 8080 user@yourcorkscrew.host`
* `proxytunnel` -> ssh tunnel
    * `ssh -p 22 -o 'ProxyCommand proxytunnel -p 192.168.1.1:<PROXY_PORT> -d
        %d:%p' -D 8080 user@yourproxytunnel.host`
    * `ssh -p 443 -o 'ProxyCommand proxytunnel -p 192.168.1.1:<PROXY_PORT> -d
        %d:%p' -H "<Browser User agent>" -H "Host %h" -H "Referer: %h" 
        -P username:password' -D 8080 user@yourproxytunnel.host`
* you can create host aliases with those commands in `.ssh/config` file
* `httptunnel` -> needs to be installed on client and host (win + linux)
* `sslscan` -> a CLI tool to check quality of SSL/TLS cert config
* `nslookup -type=mx gmail.com` → discover DNS MX record (Email Exchange)
* checktls.com -> handy site to check certificates


How to protect against social attacks:

* view email as text
* use things like `ublock`
* isolation and compartmentalisation
* use virtual machines to open suspicious files, emails etc
* use application execution controls
* sandboxes
* use common-sense

cipher suite:
→ good choice : elipctical curve + DH
