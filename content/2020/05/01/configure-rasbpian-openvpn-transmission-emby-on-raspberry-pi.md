---
draft: true
title: "Configure Raspbian, OpenVPN, Transmission & Emby on Raspberry PI"
description: "Can't get better than this"
slug: "configure-rasbpian-openvpn-transmission-emby-on-raspberry-pi"
date: "2020-05-01T20:05:24+01:00"
toc: true
toc_levels: 1
categories:
  - unix
tags:
  - linux
  - rpi
  - emby
---


loga
https://www.raspberrypi.org/app/uploads/2012/03/raspberry-pi-logo.png
https://raw.githubusercontent.com/MediaBrowser/Emby.Resources/master/images/Logos/logoicon.png
https://joscor.com/wp-content/uploads/2013/06/openvpn-logo.png
https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Transmission_Icon.svg/600px-Transmission_Icon.svg.png


## reqs

```
sudo vim /etc/sysctl.conf


sudo vim /etc/netplan/00-snapd-config.yaml
sudo vim /etc/netplan/50-cloud-init.yaml

sudo vim /etc/sysctl.conf
sudo sysctl -p


sudo vim /etc/host.conf
sudo vim /boot/config.txt


sudo apt install transmission-daemon transmission-cli
sudo systemctl stop transmission-daemon.service
sudo usermod -a -G ubuntu transmission-daemon
sudo vim /etc/sysctl.d/20-transmission.conf
sudo vim /etc/transmission-daemon/settings.json
sudo vim /etc/systemd/system/transmission-daemon.service.d/run-as-user.conf
vim ~/.config/transmission-daemon/settings.json
sudo systemctl daemon-reload
```


## Disk

```shell
mkdir ~/disk
sudo fdisk -l
sudo vim /etc/fstab
sudo mount /dev/sda1 /home/ubuntu/disk/
```

## VPN

```shell
sudo service openvpn restart
cd .openvpn/
sudo mv sweden.ovpn /etc/openvpn/
sudo mv up /etc/openvpn/
sudo mv use-pihole-dns.sh /etc/openvpn/
sudo mv sweden.ovpn sweden.conf

sudo vim /etc/default/openvpn

sudo iptables-restore < /home/ubuntu/.iptables/ipv4rules
sudo ip6tables-restore < /home/ubuntu/.iptables/ipv6rules

sudo iptables-persistent
sudo iptables-save
sudo systemctl enable openvpn@client
sudo systemctl deamon-reload
sudo systemctl start openvpn@sweden

wget -qO- http://ipecho.net/plain && echo

```


## Emby

```
wget https://github.com/MediaBrowser/Emby.Releases/releases/download/4.3.0.9/emby-server-deb_4.3.0.9_armhf.deb
sudo dpkg -i emby-server-deb_4.3.0.9_armhf.deb

```


Get rid of cloud service
```shell
sudo vim /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
sudo touch /etc/cloud/cloud-init.disabled
sudo systemctl stop cloud-init.service
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock

sudo apt-get purge cloud-init
sudo rm -rf /etc/cloud/; sudo rm -rf /var/lib/cloud/
```


Run `emby` as different user:
```shell
sudo chown -R ubuntu:ubuntu /var/lib/emby/
sudo systemctl disable emby-server --now
sudo systemctl enable emby-server@ubuntu --now
```
