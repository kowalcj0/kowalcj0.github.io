---
draft: false
title: "Ethical Hacking - Enumeration"
slug: "ethical-hackin-enumeration-course-notes"
date: "2018-02-02T19:20:50+01:00"
categories:
  - security
  - learning
tags:
  - security
  - enumeration
  - ethical hacking
  - pentesting
cover:
  image: /img/2018/004/ethical-hacking-wikimedia.jpg
  style: normal
---

Not much content here apart from just a bunch of notes I took during
learning.


# Introduction

## Protocols/Technologies used in Enumeration

* DNS (port 21)
* SMTP (port 161)
* RPC
* NetBIOS (port 139)
* SMB (port 444)

## Protection Rings

Every OS has it's own set of `Protection Rings` -> [for more see wiki](https://en.wikipedia.org/wiki/Protection_ring)

### Windows Kernel Protection rings
* Ring 0 - kernel mode
* Ring 1 & 2 - in windows it's traditionally unused now it\s used for virtualization like Intel VtX
* Ring 3 - user mode

### OpenVMS
has 4 rings:
* Ring 0 - kernel
* Ring 1 - executive
* Ring 2 - supervisor
* Ring 3 - user

### ARM
* Ring 0 - application - least privilaged level
* Ring 1 - operating system
* Ring 2 - hypervisor - the most privilaged level


# Basics of Enumeration

## User accounts on:

### Windows
* Root user - account is called SYSTEM
* System administrator
* User administrators

### Linux
* Users are identified by `UIDs`
* Root has uid=0 ( `echo $UID` )
* All other user accouunts with UIDs can be found by `cat etc/passwd`
* UIDs are in column 3
* Users with root access can be found in: `cat /etc/sudoers`

### NetBIOS
it's a windows protocol that provides session layer service
runs on ports:

* NetBIOS Name Service: port `137 UDP`
* Datagram distribution service: port `138 UDP`
* NetBIOS over TCP/IP: port `139 TCP`

### SMB Server Message Block
It's a application layer service used to enable shared accounts to accounts, 
printers etc between nodes in a network

`SAMBA` is a free Linux implementation of SMB, which can integrate with 
`Windows` SMB nodes

### RPC
it's a Client-Server framework based on Remote Procedure Call mechanism `DCE/RPC`

Microsoft implementation of `DCE/RPC` is an extended version of `DCE/RPC` that
runs over SMB over TCP/IP.
All following Windows Server domanin protocols are based on DCE/RPC:

* DNS administation
* MS Exchange
* MAPI


# Local Host Enumeration


## Basic Linux profiling

List of handy commands that will allow you to find out more about the linux host:

* `uname -a` -> get basic kernel info
* `cat /proc/version` -> distro version info
* `cat /etc/*-release` -> distribution release info
* `cat /proc/cpuinfo` -> cpu info
* `df -a` -> disk space info
* `df -h` -> human friendly disk space summary
* `cat /etc/shells` -> list available shells
* `whoami`
* `pwd`
* `id`
* `users` -> list users logged in on the systems
* `cat /etc/passwd` -> to find out all users registered on the system
* `cat /etc/shadow` -> list password hashes
* `pinky` -> logging time ans src IP
* `pinky -l phillip` -> find out more about specific user
* `finger` -> can be used if `pinky` is not present
* `w` -> info about users and their current running process (like terminal)
* `who -a` system level view of processes
* `last` -> current user activity history
* `lastlog` -> all users logging in activity history
* `ps e`, `ps aux` -> get list of running processes
* `top` -> list all running processes
* `dpkg -l` -> list all installed packages


## Basic local host/network profiling

* `ifconfig`
* `route`
* `iptables -L`


## PsTools tools on Windows

* `psInfo` -> basic system info, os version, uptime, cpu info etc
* `psInfo -d` -> more info, including shares & rpcs
* `psInfo \\10.0.2.5` -> enumerate remote host using the same username & password as current user
* `psInfo \\10.0.2.5 -u OtherUser -p OtherUserPassword` -> enumerate remote host using other user credentials
* `psInfo -s` -> list all installed software
* `psList` -> enumerate processes
* `psList \\10.0.2.5` -> enumerate processes on remote host
* `psList -t` -> list processs as tree
* `psList -x` -> full thread details and mem details, kernel info, very detailed
* `psLogList -n 20` -> limit the enumeration of events to N entries
* `psLogList -d 1` -> limit the enumeration of events to N days
* `psLogList -m 3` -> limit the enumeration to N last however minutes
use `-b` for before or `-a` for after switches to limit the events before or after certain time
* `psLogList -x` -> to extend the list with hex dump of the event
* `psLoggedOn \\10.0.2.5` -> check who's logged on
* `psService` -> list running services
* `psService \\10.0.2.5 security EventSystem` -> check security configuration for specific service, shows info about all users who can manipulate the service and actions that can be taken
* `psService \\10.0.2.5 depend EventSystem` -> check which other services depend on this one


## Basic netwrok enumeration on Windows

* `net view` -> enmerate basic machine info and domanin names
* `net view /domanin` -> provides info on the domain the sys is connected
* `netstat` -> shows active TCP connections, just like on linux
* `netstat -a` -> will include listeners (both ipv4 and ipv6)
* `netstat -a -p UDP` -> limit output to UDP listeners
* `netstat -a -p UDPv6` -> limit output to UDP listeners via IPv6
* `netstat -a -p TCPv6` -> limit output to TCPv6
* `netstat -abop TCP` -> show process ownership and process name
  * `lsass.exe` -> authentication service on windows
* `netstat -s` -> shows summary statistics, number of active, passive & failed connections etc
* `netstat -rn` -> shows routing info + remote ip address in numeric form 


## Basic netwrok enumeration on Linux

* `netstat -i` -> show active network interfaces
* `netstat -ie` -> show extented info about active network interfaces
* `netstat -rn` -> shows routing info
* `netstat -a` -> shows all connections, icnluding linux sockets & listeners
* `netstat -t` -> limit to just TCP connections
* `netstat -au` -> limit to just active UDP connections
* `netstat -nt` -> shows TCP connection in numeric addresses
* `netstat -tp` -> include owning process info of TCP connections
* `netstat -lx` -> shows all listening ports
* `ss -t` -> enumerate netwrok sessions, established sessions and local & remote port info
* `ss -nt` -> enumerate netwrok sessions, established sessions and local port info. use numeric port addresses
* `ss -tr` -> resolve remote hostnames
* `ss -t dst 132.181.109.79` -> list all tcp connections by destination addres
* `ss -t src 132.181.109.79` -> list all tcp connections by source addres
* `ss -t port eq :3243` -> list all tcp connections by source port number
* `ss -t dport eg :http` -> list all tcp connections by destination common protocol name
* `ss -t dport eg :80` -> list all tcp connections by destination port number
* `ss -t state established` -> list all established tcp connections
* `ss state established` -> list all established tcp connections including internal linux sockets
  *  `ss state` accepts other connection states: established, synsen, synrecived, finwait...


# Remote Host enumeration


## nmap

* `nmap -PS 10.0.2.1` -> enumerate available ports on remote host
* `nmap -sU 10.0.2.1` -> check which services are listening on UDP ports (goes through all 65K ports, so it's pretty slow)
  * if nmap says that a port in `open|filtered` state, it means something, like a firewall, filter or other network obstable is blocking it and it can't say whether it's open or not.
* `nmap -sTUV -p T:21-139,U:53,11,137,2049 10.0.2.1` -> provide info on services on selected TCP (T) and UDP (U) ports. If possible it will provide also info on service version.

## nmbtscan

Scan Samba services:

* `nbtscan -v -s : 10.0.2.0/24` -> scan selected network for samba. listing of systems active on the network and their netbios names, along with the name of the service usage, like `:00U` is a workstation, `:00G` is a domain name, `:20U` file serve service, `:1du` and `:1eG` are master browser.
* `nbtscan -rv 192.168.1.4` -> run a scan against a single node. Provides the same info as the previous network scan command but in slightly different format.

## scan samba resources with nmap scripts

You can find nmap scripts for samba in: `ll /usr/share/nmap/scripts/smb*`

* `nmap --script smb-os-discovery 192.168.1.11` -> lists open ports on the target host, OS details. You can use it against Windows & Linux hosts.
* `nmap --script smb-enum-users 192.168.1.11` -> lists user accounts on remote samba node. many of default Windows user accounts are disabled. (this scirpt uses Null session to obtain user accounts, it won't work against e.g. Win 10, as such access was disabled.)

## enum4linux

* `enum4linux -U 10.0.2.6` -> get user list (agains metasploitable node), open ports, infor about services and also checks if system allows session with blank username and password
* `enum4linux -S 10.0.2.6` -> enumerates available shares.
* `enum4linux -a 10.0.2.6` -> perform a full set of enumerations (including NBT stat info, user accounts, shares, password policy info and readclycling )


## smbmap (kali)

* `smbmap -u training -p training -H 10.0.2.6` -> establishes a Samba session and enyumerates the shares.
* `smbmap -u '' -p '' -H 10.0.2.6` -> run scan with Null session details
* `smbmap -u '' -p '' -H 10.0.2.6 -R` -> list directory listing in temp share

## shareenum 
* `shareenum -o shares1.txt 10.0.2.6` -> run scan using `Null` session and save results list of found file shares in shares1.txt (it's a CSV file) 
* `shareenum -o shares1.txt -u username -p password 10.0.2.6` -> run scan using specific account
* `shareenum -o shares1.txt -u username -p password 10.0.2.6` -> run scan using specific account

## rpcclient (linux)

Comes as part of `samba` suite. It needs authenticated access (no support for Null sessions).

* `rpcclient 10.0.2.5 -U IEUser` -> will start an interactive session
* `rpcclient` commands in interactive session:
    * `help`
    * `srvinfo`
    * `getusername`
    * `enumdomusers` -> provides list of user with their IDs in hex form
    * `queryuser 0x1f4` -> query user account by UID in hex
    * `queryuser 500` -> use decimal UID instead hex
    * `enumprivs` -> list se of priviliges on the system
    * `enumdomgroups` -> list domain groups
    * `enumalsgroups builtin` -> enumerate alias groups
    * `netshareenum` -> enumerate shares
    * `netshareenumall` -> enumerate shares incluing the system ones
    * `enumprinters` -> enum printers on the host
    * full list of `enum` commands is available after typing `enum` and pressing `TAB` twice

## Other enumeration tools

* `NetBios Scan` -> It's a simple Windows GUI `NetBios` scanner that can also enumerate shares.
* `ShareEnum` -> from windows sysinternals. Very simple tool to discover shares in a workgroup.
* `DeepNetScanner` -> Another name for `NetBios Enumerator` tool. A Windows GUI `NetBios` scanner.
    * It provides more information than `NetBios Scan`. 
    * Supports `Null Sessions`
* `MiTec Network Scanner` -> Very nice scanning tool with plenty of scanning options.
    * Can perform:
        * regular port scanning
        * or dedicated ICMP, NetBios, SNMP, WMI, Registry, Active Directory scans.
    * Can be used to scan:
        * netwotrk neighborhood
        * IP Network range
        * Active Directory
* `SoftPerfect Network Scanner` -> allows for:
    * TCP/UDP port scanning, enumeration of:
        * Samba
        * WMI
        * SNMP
        * NTTP
        * NetBios
        * DNS
        * NTP
        * MSSQL
        * TFTP
        * NBNS
        * Radius
        * Windows Shares (including a check for write access)
    * It has a lot of handy filtering and scanning options.
    * You can also control:
        * samba based services
        * user accounts
        * shares
        * remote hosts via standard windows `Computer Management` GUI console
    * Explore remote file systems whenever possible


## SNMP enumeration

It's a internet standard since 1990.  
Information in SNMP is given in OID (object identifiers) `1.3.6.1.2.1.2.2.1.8`  
Most devices are shipped with two `community strings`: 

* `public` which provide a read-only access to various metrics or settings
* `private` which gives a read/write access

Community name is frequently used when accessing objects (OIDs).  
To identify the OIDs you need to have a correct MIB database for specific device/system.
You can find a lot of MIBs on:

* `Packet Storm` [https://packetstormsecurity.com/](https://packetstormsecurity.com/)
* `mibDepot` -> [http://www.mibdepot.com](http://www.mibdepot.com)
    * it has over 12000 SNMP MIBs & more than 1.8 million MIB object definitions


### scanning SNMP running on Linux

Once you have a file (e.g. `linux.txt`) with OIDs specific to your device in a form of:

```csv
Linux     RUNNING PROCESSES      1.3.6.1.2.1.25.4.2.1.2
Linux     SYSTEM INFO            1.3.6.1.2.1.1.1
...
...
```

You can use a perl `snmpenum.pl` script to enumerate host via SNMP.
```shell
perl snmpenum.pl 10.0.2.6 public linux.txt
```

### scanning SNMP running on Windows

`SNMP` on Windows is disabled by default.  
You have to turn on a `Simple Network Management Protocol (SNMP)` & 
`WMI SNMP Provider` Windows feature via `Programs and Features` in `Control Panel`.  
Once enabled, you will see `SNMP Service` running `C:\Windows\System32\snmp.exe`.  
In the Security tab on service properties, you can toggle authentication, 
and toggle access from any of from selected hosts and define i.e. `READ ONLY` 
community string `public`.

You can use the same perl script to windows host:
```shell
perl snmpenum.pl 10.0.2.6 public windows.txt
```

Above script should list:

* listening TCP ports
* user accounts
* running processes
* listenting UDP ports
* uptime
* installed software
* services on the system
* sys info
* hostname
* disks & shares


## RPC

* `uuidgen -r` -> display unique UUID and can be included in the rpc client.

`MS Windows Server Resource Kit tools` -> comes with a set of few `RPC` tools:

* Rpccfg.ex
* Rpcdump.exe
* Rpcping.exe
* RPing

* `rpcdump /i | more` -> list all registered endpoints dived into three groups:
    1. Connection oriented TCP/IP
    2. named pipes
    3. local RPC [For TCP connections, listening port is in square brackets]
* `rpcdump /i /v | more` -> use more verbose mode. It prints out a lot of info
* `rpcdump /i /v /s 10.0.2.4 | more` -> scan remote host


### Winfingerprint from QP Download

It's a GUI RPC scanner with quite a few scan options.  
Shows RPC bindings for both tcp and udp endpoints.


### Unix RPC mapper on port 111

This tool comes preinstalled with Kali

* `rpcinfo -p 10.0.2.6` -> provides a listing of tcp & udp endpoints, port number and service managing them
* `nmap --script rpcinfo 10.0.2.6` -> the same information can be obrained using `nmap` script that will enumerate port 111


### WMI, WBEM & CIM

* `WMI` - Windows Management Instrumentation (WMI uses CIM to represent systems, applications, networs, devices & other managed components)
* `WBEM` - Web-Based Enterprise Management
* `CIM` (Common Information Model) - is developed & maintained by DMTF Distributed Management Task Force

All WMI objects are queried using WMI querying Language (WQL - similar to SQL).  

* There are persistent and dynamic (generated on the fly) WMI objects
* Persistent object are stored in the CIM repository, located in: `Windows\System32\wbem\Repository\OBJECTS.DATA`.
* `WMI service` is started by deafult in Windows.

MS provides two prtocotls to transmit WMI objects remotely: 
`DCOM` & `Windows Remote Management WRM`. 
DCOM is default protocol, which establish initial connection over port `135`, 
and then negotiates a random service port for further communication 
(can be hardcoded to a static port though).  
Some WMI objects contain methods, that can be executed!!! e.g. `create()` 
method of `Win32 Class`.  
WMI also provides `eventing` system. Users can register events on creation,
modification or deletion of any WMI object.  
Many obsucre WMI classes are not officialy documented on MSDN (search for 
MSDN Win32 Classes).  

All WMI classes are organised hierarchicly and grouped into namespaces.  
WMI  classes are frequently used during many phases of the attack life cycle:

* reconaisance
* AVVM detection
* code execution
* latteral movement
* cover data storage
* introduction of a backdoor
* persistance

Example usage:

* `Get-WMIObject Win32_Account | select name,__Class` -> a complete list of group, user, system accounts.
* with simple powershell script you can get info about remote disk size etc.

##### MS tools to browser WMI DB

* `wbemtest` will launch a GUI app that allows you to browse the WMI classes.
* `WMI Explorer` get it from codeplex.com. Provides a nice GUI to browse the WMI Classes in a tree view. 

Interesting classes from:

`ROOT\CIMV2` tree:

* Win32_BIOS
* Win32_DiskDrive
* Win32_LogicalDisk

`ROOT\SecurityCenter2` tree:

* AntiSpywareProduct
* AntiVirusProduct
* FriewallProduct

### WinRM

WinRM (remote management) is enabled on port TCP `5895` HTTP with encryption 
turned on by default. HTTPS can be configured over port `5896`.

Using PowerShell:

* `Test-WsMan -ComputerName 10.0.2.10` -> a standard WMI banner will be displayed if tool can connect to the remote host via WinRM
* `Get-WMIObject Win32_Account  -ComputerName 10.0.2.10 | select name,__Class` -> a complete list of group, user, system accounts from the remote system.


## Finger

`finger` is a legacy service that runs on port `79` and is not installed by 
default on new Linux boxes.
So you can find it on fairly old OSes.

This tool allows to enumerate users on local or remote linux hosts:

* `finger -l malcolm@10.0.20.9` -> shows user: name, login, $HOME, shell, last login time, inf about mail and plans
* `finger -l @10.0.20.9` -> shows logged in users on remote system.
* `finger -l root@10.0.20.9` -> get info about user that is not currently logged id. You have to know it's ID/login.


# Enumerating the Internet

## Tracing

* on Linux `hping3 --traceroute -V -1 66.32.101.17` -> shows regular traceroute to a host
* on Windows `tracert 66.32.101.17` 
* [Open Visual Traceroute](http://visualtraceroute.net/) - shows the traceroute on a globe map


## Shodan

Handy queries:

* `net:"132.181.106.0/24"` -> get info about the whole network
* `net:"132.181.106.0/24" port:"80"` -> find http servers in specific network


## ZMap

[zmap](https://ZMap.io) is an open-source netwrok scanner. It's very efficient and fast.

By default `zmap` will perform a `tcp-syn` scan on specific port on maximum rate possible.

* `zmap -p 80 -n 100 -o web1.txt` -> scan 1000 random hosts on the winternet listening on port 80 and save results to file `web1.txt`
 * `zmap -p 80 66.77.0.0/16 -r 200 -o web2.txt` -> scan specific network at a maximum rate of 200 requests per second. It can enumberate the whole class B IP address network on a DSL in just few minutes.

*NOTE:*  
Running `zmap` in an uncotrolled manner is very noisy, and when the rate 
limiting is not set properly, then packets can get lost and results will be incomplete.


# Other Enumeration Tools

## SuperScan
`SuperScan 4.1` is available from McAfee website. It's a Windows GUI application that can scan hosts, IP ranges.
It can extract a lot of info about Windows hosts but it's not always correct as sometimes it can misinterpret hosts, OSes etc. due to the fact it's not actively maintained.

## NetScan Tools Pro

You can scan the targets by: hostname, ip & EMAIL address (interesting).
Can perform various automatical scans, ports, samba shares, dns scan setc. 
but you can also perform more manual scans against.


## LDAP

LDAP holds data in a tree structure DB, allows for searching for poeple, devices, printers etc. in the organisation
```ascii
       Root
        |
        ↓
    Country
        |
        ↓
   Organization
        |
        ↓
 Organizational Unit
        |
        ↓
 Individual Entity
```

LDAP directory can be distributed across many servers each having a replicated version of the directory which is synced periodically.

`OpenLDAP` - It's a open-source LDAP server for linux.
By default `OpenLDAP` allows for anonymous access. Very risky. Anyone can view the directory contents.


### Other LDAP Scanners

* [JXplorer](http://jxplorer.org/) - Open source Java GUI tool.
* [LdapMiner](https://sourceforge.net/projects/ldapminer/)
* [nmap](https://nmap.org/)
    * `nmap -p 389 --script=ldap-search 10.0.2.9` -> enumerates the whole LDAP DB.

### Using telnet to access LDAP

* `telnet 10.0.2.6 25` -> connect to 
    * `vrfy anthony` -> will return `5.1.1` if user account doesn't exists or `2.0.0` if it does
    * `mail from: anthony` -> check if there's an email sent from selected account
    * `recp to: mail` -> we can check for the existence of emaill address:
        * `2.1.5` response code means success
        * `5.1.1` means that the sought account doesn't exist.
        * This technique can be used to detect whether provided email addresses are active or not in a SMTP system.

