#!/bin/bash
set -euo pipefail

if [ ! -f flag.txt ]; then
    echo "hxp{dummy}" > flag.txt
fi

if [ ! -f image.iso ]; then
    wget https://github.com/klange/toaruos/releases/download/v2.2.0/image.iso
fi

echo "c67238138f47e960eaeabe097debb4fb10c40d09d722b87d4ce9538a9ef3af5b image.iso" | sha256sum --check --strict --status

bsdtar -xf image.iso kernel ramdisk.igz

tar -xf ramdisk.igz etc/master.passwd
sed -i "s/root:toor/root:$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 22)/g" etc/master.passwd
sed -i "s/local:local/local:$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 22)/g" etc/master.passwd
sed -i "s/guest:guest/guest:$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 22)/g" etc/master.passwd
zcat ramdisk.igz > ramdisk
tar --delete -f ramdisk etc/master.passwd
tar -rf ramdisk etc/master.passwd flag.txt --mode=400 --owner=0 --group=0

gzip -c ramdisk > ramdisk.igz

rm -rf ramdisk etc
