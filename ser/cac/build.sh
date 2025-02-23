#!/bin/bash

# tar -xf ramdisk.igz etc/sudoers
# echo "root" >> etc/sudoers
zcat ramdisk.igz > ramdisk
tar --delete -f ramdisk etc/sudoers
tar --delete -f ramdisk etc/master.passwd
tar --delete -f ramdisk home/local/a.krk
tar --delete -f ramdisk home/local/exploit
tar -rf ramdisk etc/sudoers --mode=400 --owner=0 --group=0
tar -rf ramdisk etc/master.passwd --mode=777 --owner=0 --group=0
# tar -rf ramdisk home/local/gcc.tgz --mode=777 --owner=0 --group=0
tar -rf ramdisk home/local/a.c --mode=777 --owner=0 --group=0
tar -rf ramdisk home/local/a.krk --mode=777 --owner=0 --group=0
# tar -rf ramdisk home/local/exploit --mode=777 --owner=0 --group=0
# tar -rf ramdisk home/local/.eshrc --mode=777 --owner=0 --group=0

gzip -c ramdisk > ramdisk.igz

rm -rf ramdisk
cp ramdisk.igz ../new.igz
