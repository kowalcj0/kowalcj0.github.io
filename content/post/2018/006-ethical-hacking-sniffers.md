---
draft: false
title: "Ethical Hacking - Sniffers"
slug: "ethical-hackin-sniffers-course-notes"
date: "2018-02-05T09:22:50+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
  - sniffers
cover:
  image: /img/2018/006/Wireshark_Logo.png
  caption: Wireshark logo
  style: wide
---
These are just my notes from the video course: "Ethical Hacking: Sniffers".

# Sniffing overview

IPS (Intrusion Prevention System) / IDS (Intrusion Detection System) monitor 
the networks for threats, intrusions and allowed protocols.  
Network admins should monitor network traffic for few minutes a day.

## Phases of Packet Analysis

1. Gather
2. Decode
3. Display
4. Analyze

**Note:**

`epan` - Ethereal Packet Analyzer - it's the packet-analyzing engine for 
Etheral/Wireshark.


## OSI Model

| Layer | Name          | Role                                                  | Protocols         | PDU       |Address|
| ----- | ------------- | ----------------------------------------------------- | ----------------- | --------- | ----- |
| 7     | Application   | Initiate contact with the network                     | HTTP, FTP, SMTP   | DATA      |       |
| 6     | Presentation  | Format data , optional compression and encapsulation  |                   | Data      |       |
| 5     | Session       | Initiates, maintains and tear down session            |                   | Data      |       | 
| 4     | Transport     | Transport data                                        | TCP, UDP          | Segment   | Port  |
| 3     | Network       | Addressing and routing                                | IP, ICMP (ARP)    | Packet    | IP    |
| 2     | Data link     | Frame formation                                       | Ethernet II (ARP) | Frame     | MAC   |
| 1     | Physical      | Data is transmitter on the media                      |                   | Bits      |       |


## IPv4 structure

{{< gallery >}}
{{< figure link="/img/2018/006/ipv4header.png" thumb="-thumb" size="683x399" caption="IPv4 headers" >}}
{{< /gallery >}}

{{< pswp-init >}}


## Passive vs Active attacks

Two types of attacks:

* Passive - e.g.: sniffing traffic, eavesdropping, traffic analysis or tapping
* Active - e.g. releasing malware, DDoS

Any attack can be aimed against any security services:

* Confidentiality - Protection of data against unauthorized disclosure, i.e.:
    unauthorized aceess to patient's data from mediacal facility
* Itegrity - Protection of data against unauthorized modification, e.g. change
    employee's salary
* Availability - Data and services are available to authorised user e.g. DDoS
* Authentication - veifying the identity of a user or device

### Passive Attacks:

* sniffing traffic, eavesdropping, traffic analysis or tapping
* monitoring transmissions
    * capture passwords and router advertisements
* can result in the disclosure of information
* reconnaissance - trying to find out information about the network, usually
    done with:
    * ping scan - use ICMP to discover which hosts answer to regular ping req
    * port scan - discover services running on a network


### Active attacks:

* Break into a secure system
* alter the integrity of the system
    * steal or modify information
    * introduce malicious code
* Denial of Service (DDoS)
* Buffer overflow - send more data to application than expected
* password attack - tries to obtain passwords stored on network account DB or
    password protected file


### Monitor and Defend:

* Prevention - use encryption for data at rest or in motion
* Detection - use IDS to detect intruders
* Policies - frequent changes of password
* Physical controls - locks and smartcards
* Device security - IDS/IPS, firewalls and switches
* User a layerd approach with various methods of defence


# Tap into stream

Thre are two basic types of ethernet environments:

* Share of hub based
* Switched network

On a Wireless network `802.11b/g/n` act like a hub and allows you to see all
traffic!!!

On wired networks to monitor the traffic you can use:

* `Port Mirroring` or `SPAN (Switched Port Analyzer`
* Full-duplex tap in line with traffic (requires a special adapter)
* wireshark is built-into the Cisco Nexus 7000 series and many other devices

## Various techniques used to sniff traffic in local networks

### ARP Spoofing

* ARP spoofing
    * ARP is stateless
    * ARP `reply` can be sent, even if there's no `request` & it will be
        accepted
    * poison the cache by spoofing the MAC address
    * so that the traffic is sent to the spoofer rather to the network switch


1. Enable IP forwarding on your host:
```bash
# echo 1 > /proc/sys/net/ipv4/ip_forward
```
2. Spoof the victim that the hacker's MAC address is the gateway
```bash
# arpspoof -t victim gateway
```
3. Spoof the gateway to believe we're the victim
```bash
# arpspoof -t gateway victim
```


# Layer 2 attacks

Many of data (2nd) layer attacks involve cisco protocols.

Example layer 2 attacks:

* macof attack
* MAC spoofing
* CDP attack
* STP attack


## macof Attack

Content-addressable memory (CAM) table:

* Maps MAC address of device to switch port
* Makes LAN more efficient, by minimizing traffic
* May hold many record pairs

`CAM table` maps the MAC address of a device to the physical switchport.  
`macof` floods the CAM table with bogus entries, so the 
switch has no way of telling where to send the data. Then Switch enters a 
`fail-open mode` and starts acting like a hub, and sends traffic out to all 
ports. This makes the traffic sniffing an easy feat.

In order to this attack to be successful:

* it must continue to flood the switch with bogus entries
* once stopped, the timers on switch will be reset
    * and switch will resort back to being a switch


## MAC spoofing

Intrusion Detection & Firewall Protection works on the Network layer or higher.
In LANs devices are identified by MAC addresses, by spoofing them we can
intercept the traffic normally directed at that devices.


## STP Attack

STP: 

* switches have redundant links
* maintains a loop-free network
* prunes redundant links
* uses Bridge Protocol Data Units

Possible Attacks:
* DoS using BPDU
* Take over the root bridge
* Claim other role

## CDP Attack

CDP - shares information with other Cisco devices.
So an attacker can use the CDP information to discover the entire topology of
the network.
This includes the iOS router and switch model types and IP addressing in order
to launch an attack.

Attacks:

* Send bogus CDP to other devices
* Flood CDP neighbours table and cause DoS

## Yersinia

A tool that uses vulnerabilities in some of the data link layer protocols,
like:

* STP
* CDP
* DTP
* DHCP
* HRSP
* ISL
* VTP
* 802.1Q
* 802.1x


## Protetect against layer 2 attacks

* macof attack defence
    * use switchport port security
        * limits the number of MAC addresses connecting to a signle port on a
            switch
        * easy to configure on cisco switch

```shell
switch(config-if)# switchport mode access
switch(config-if)# switchport port-security
switch(config-if)# switchport port-security
mac-address { <mac_addr< | sticky }  # chose sticky
switch(config-if)# switchport port-security
violation { protect | restrict | shutdown } # `shutdown` is recommended
```

* **MAC spoofing defence:**
    * enable `Source Guard` on a Cisco device
        * this turns on filtering on trusted IP and MAC address bindings
        * to circumvent this protection, an attacked would have to spoof both
            MAC address & IP address (which is a bit more difficult)
* **CDP attack defence:**
    * it's a passive attack so there's not much that can be done except:
    * disabling it or using it only when required
* **STP attach defence:**
    * disabling it is not a good idea as we could get looping effect
    * use `Portfast`
    * then configure `BPDU-guard` which disables the port from reciving BPDUs
    * `(config)# spanning-tree portfast bpduguard`
    * lastly enable `Root Guard`
    * `(config)# spanning-tree guard root`

# DHCP

DHCP Uses UDP for transport.  
Clients uses port `68` and Servers port `67`

DHCP process (sometimes called `DORA` process):

1. **D**iscover
2. **O**ffer
3. **R**equest
4. **A**cknowledgement


Both DHCP client & server don't have option to verify (autheticate) each other.  
You can reduce risk by:

* monitor for trusted hosts
* implementing VLAN Access Control List (VACL)
* Authorize DHCP server in Active Directory before they can release addresses
    to clients
* Dynamic ARP inspection
    * will reject invalid and malicious ARP packets
* DHCP Snooping
    * requires to build a DHCP Snooping Database first
        * it contains information learned per port, like IP, MAC & VLAN
    * on a witch works with IP Source Guard & Dynamic ARP inspection
    * relies on the concept of trusted ports & untrusted ports
    * Trusted ports -> connect to authorized DHCP servers and switch uplinks
    * Untrusted ports -> user access ports


**NOTES:**  
In `Wireshark` to view DHCP datagrams use `bootp` filter.

To renew IP address lease on Windows, use:

```shell
ipconfig /release
ipconfig /renew
```

To enable DHCP server on a Cisco router:

```shell
# enable DHCP server and relay features on the router
R1(config)# service dhcp
# specify which addresses should be excluded from DHCP pool (for devices that
use static IP addresses, like some printers etc.)
R1(config)# ip dhcp excluded-address 192.168.5.1
# give a name to a DHCP address pool
R1(config)# ip dhcp pool jasper_pool
# configure network and mask
R1(dhcp-config)# network 192.168.5.0 255.255.255.0
# specify IP address of the DNS server available to any DHCP client
R1(dhcp-config)# dns-server address 192.168.5.1
# specify default router for DHCP client
R1(dhcp-config)# default-router 192.168.5.1
# specify the IP address lease time (usually 1 day)
R1(dhcp-config)# lease 0 5 30
```

## DHCP Depletion

This can happen when:

* the setting may include one lease per client
* DHCP server has many reserved leases (can lead to unbalanced DHCP addresses)
* the scopes have uneven lease time
* the scopes have uneven sizes
* there's an influx of new users on the network


## DHCP starvation attack - DoS

Such attack exhausts all usable IP addresses on a subnet and prevents any new
user from using the network.

* Yersina can send multiple `DISCOVER` packets
* The server tries to reply with a `DHCPOFFER` to non-existent MAC address
    * deletes the IP address pool

**Defence:**  

* DHCP snooping
* Port security


## Rogue DHCP server

* Can be an effective man-in-the-middle attack
* Can supply clients with bogus information
* Point victims to wrong or hostile DNS server or default gateway
* The victim may be unaware that they have the wrong information
* `Yersinia` has an option to run a rogue DHCP server and capture traffic

## Rougue DNS server

* Attacker can redirect users to phishing websites in order to obtain sensitive
    data


# ARP spoofing (or ARP cache poison)

You can use `ethercap` to start a mitm attack with ARP poisoning.
Once you're mitm then you can try to do i.e.: an SSL strip

**Defence:**  

* use [SNORT](https://www.snort.org) IDS with `ARP Spoof Preprocessor`
* use [Arpalert](www.arpalert.org) - compares the mac addesses it detected with
    a pre-configured list of authorised MAC addresses. If MAC is not in list ,
    then arpalert will run a pre-defined user script with the MAC address & IP
    address as parameters.
* use `arpwatch` command -> check `man arpwatch`
* use [arpon](arpon.sourceforge.net) it's a ARP Handler Inspection that helps
    to avoid MITM attack through ARP spoofing/ARP case poisoning/ART poison
    routing attack.
* [XArp](www.xarp.net) works on windows

**TIPS:**  

* [asecuritysite.com](asecuritysite.com) has various `PCAP` files with various
attacks recorded.
* PCAP heaven also has a lot of PCAPs with various attacks.


# DNS

DNS uses:

* UDP port 53 for requests
* TCP port 53 for zone transfer

DNS Header consists of four sections:

* Questions
* Answer resource records
* Authority resource records
* Additional resource records

Types of DNS queries:

* `A` - IPv4 address query
* `MX` - mail exchange query
* `AAAA` - (quad A) IPv6 address query

Types of DNS servers:

* Authoritavie server
    * Contains a master set of data that publishes DNS data
    * Is updated when there's a change in the data
* Non-authoritative server
    * Cache server that retrieves DNS data
    * Contains copies of normal back and forth user queries

Attacking DNS

* Attacker can poison the cache to lauch and attack on DNS
* Change record on the authoritative server (which is a more effective attack)

Display DNS cache:
* `ipconfig /displaydns` -> shows all caches DNS entries, that contain Record
    name, type, TTL (how many seconds the record can live in the cache), data 
    lenght, IP address (A host record) & CNAME

## DNS Cache Poisoning

* Inserts bogus information into a DNS server's cache
* Achived by replying to a DNS request with a spoofed IP address
* Then the result is place in the DNS server cache until TTL expires

### DNS Cache Poisoning Effects

* In an organisation: all local users will be affected
* An ISP cache poisoning: will have widespread effects

### Defence against DNS attacks

* Enable `cache locking` -> control how DNS cache can be overwritten
* Keep your systems patched and updated
* Disable unnecessary services on the machine
* Cache server should have different IP address from the authorative DNS server
* If you user Domain Name Registrar
    * use Two-factor auth
* Implement extra type of verification 'ere you make any change to the config
* Use DNS Security Extensions
    * They provide origin authentication and data integrity
* Protect DNS Resolver
    * It manages DNS requests for all clients on your network
    * Restrict access to users on your network
    * Check if there are other open DNS resolvers in your network

# Other tools

*Linux snffiers:*

* tcpdump
* Ettercap - handy for switched LANs
* dsniff - can sniff a variety of objects on a network

# Defence against sinffing

* Disable any open ports in common areas
* user encryption for email, web pages, http transactions or configuring
    devices (ssh)
* Use programs like:
    * AntiSniff -> detects if a node is in promiscouous mode
    * Arpwatch -> monitors ARP cache
    * Snort -> it's an IDS which has a arpspoof preprocessor 
    * Who's on My WiFi -> it's a windows tool (rather useless imho)
