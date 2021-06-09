---
title: "Install Digikam in Truenas Jail"
description: "Install Digikam in Truenas Jail"
date: 2021-06-09T21:52:01+01:00
draft: false
toc: true
slug: "install-digikam-in-truenas-jail"
categories:
  - unix
  - photography
tags:
  - freebsd
  - trunas
  - jail
  - digikam
cover:
  image: ../digikam_oxygen.svg
  caption: ""
  style: normal
---


## 1 - Create new jail 

Use Web GUI or CLI to create a new jail according to your liking.

I'm going to do it via Web GUI with `NAT` and `NAT Port Forwarding` enabled.  
I'll also add a port mapping for ssh from jail's tcp port `22` to host's `22222`.

## 2 - Get ports

Connect to the newly created jail so we can fetch and extract ports:

```shell
iocage console digikam
portsnap fetch
portsnap extract
```

## 3 - Install dependencies

At this point, it might be worth to install `xauth` which will be required to start
`digikam` via ssh with X11 Forwarding enabled and `vim` to edit few config files.

```shell
pkg install xauth vim
```

Now, the meaty part.  
You can follow the official [freshports installation instructions for digikam](https://www.freshports.org/graphics/digikam/):

```shell
cd /usr/ports/graphics/digikam/ && make install clean
```

But this process will take ages as you will be prompted multiple times for build options for
all digikam's dependencies and later on it will take ages to compile all of them.

To save yourself that trouble you can generate a list of digikam's dependencies and
install them with `pkg`.  

```shell
cd /usr/ports/graphics/digikam/
pkg install `make all-depends-list | cut -d / -f 4,5`
```

If you'll get an error saying that following packages couldn't be found:

* math/suitesparse-umfpack
* math/suitesparse-amd
* math/suitesparse-config
* math/suitesparse-camd
* math/suitesparse-colamd
* math/suitesparse-ccolamd
* math/suitesparse-cholmod
* textproc/py-gi-docgen
* textproc/py-smartypants
* textproc/py-typogrify
* math/Imath

Save the list of all (700+) dependencies in a sorted file:

```shell
make all-depends-list | cut -d / -f 4,5 | sort > reqs
```

and remove missing ones from `reqs` file

Finally, install the dependencies with:

```shell
pkg install `cat reqs`
```

## 4 - build and install digikam

We can finally build and install `digikam` with:

```shell
make install clean
```

## 5 - Add digikam user

Create new `digikam` user with `adduser`. 

Remember to set `GID` to same value as the account you normally use to manage your photos. 
In my case it's `1001`.

```shell
# adduser
Username: digikam
Full name: digikam
Uid (Leave empty for default): 1001
Login group [digikam]:
Login group is digikam. Invite digikam into other groups? []:
Login class [default]:
Shell (sh csh tcsh bash rbash git-shell nologin) [sh]: bash
Home directory [/home/digikam]:
Home directory permissions (Leave empty for default):
Use password-based authentication? [yes]:
Use an empty password? (yes/no) [no]:
Use a random password? (yes/no) [no]:
Enter password:
Enter password again:
Lock out the account after creation? [no]:
Username   : digikam
Password   : *****
Full Name  : digikam
Uid        : 1001
Class      :
Groups     : digikam
Home       : /home/digikam
Home Mode  :
Shell      : /usr/local/bin/bash
Locked     : no
OK? (yes/no): yes
adduser: INFO: Successfully added (digikam) to the user database.
Add another user? (yes/no): no
Goodbye!
```

You can now create a `Pictures` directory as root:

```shell
mkdir /home/digikam/Pictures
chown digigam:digikam /home/digikam/Pictures
```

or do it as `digikam` user:

```shell
su - digikam
mkdir ~/Pictures
```

## 6 - Enable and configure ssh

Let's start with editing `ssh` daemon configuration `/etc/ssh/sshd_config`.

Here's an example config that enables `X11 Forwarding` and password-less login:

```shell
AcceptEnv LANG LC_*
AllowUsers digikam
AuthorizedKeysFile      .ssh/authorized_keys
ChallengeResponseAuthentication no
PermitRootLogin no
Port 22
PrintMotd yes
Subsystem       sftp    /usr/libexec/sftp-server
UsePAM yes
X11Forwarding yes
```

We can now enable `ssh` by adding `sshd_enable="YES"` to `/etc/rc.conf`

PS. if you don't like IPv6 like me, turn it off: `ipv6_activate_all_interfaces="NO"`

Once done, switch to `digikam` user with `su - digikam` and add you public key to `~/.ssh/authorized_keys`.

Finally, exit and stop the jail so you can add a mount point via WEB GUI from your pictures
directory to newly created `~/Pictures` which should be located under: 
`/mnt/jails/iocage/jails/digikam/root/usr/home/digikam/Pictures`.

## 7 - Create a handy shortcut to remote digikam

Create a new desktop file: `~/.local/share/applications/digikam-nas.desktop`

```
[Desktop Entry]
Version=1.0
Type=Application
Name=Digikam NAS remote
Icon= ~/.icons/digikam_oxygen.svg
Exec=ssh -X digikam@<YOUR_NAS_IP_OR_DOMAIN_NAME> -p 22222 digikam
Comment=Digikam photo manager
Categories=Photography;
Terminal=false
```

Once saved, you should see a new entry in your application launcher.

If you're on Gnome and the digikam launcher doesn't show up, then restart it with:
`Alt+F2`, enter `r` and hit `Enter` key.

You should now see `Digikam NAS remote` enty in your application launcher.

