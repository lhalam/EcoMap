#!/usr/bin/env bash

VBGAVERSION=5.1.18

sudo apt-get update -y

sudo apt-get dist-upgrade -y

sudo apt-get install linux-headers-$(uname -r) build-essential dkms -y

sudo wget -c http://download.virtualbox.org/virtualbox/$VBGAVERSION/VBoxGuestAdditions_$VBGAVERSION.iso \
-O /opt/VBoxGuestAdditions_$VBGAVERSION.iso > /dev/null 2>&1

sudo mount -o loop,ro /opt/VBoxGuestAdditions_$VBGAVERSION.iso /mnt

echo "yes" | sudo sh /mnt/VBoxLinuxAdditions.run uninstall

echo "yes" | sudo sh /mnt/VBoxLinuxAdditions.run --nox11

sudo groupadd vboxusers

sudo usermod -a -G vboxusers $USER

sudo umount /mnt

sudo rm /opt/*.iso
