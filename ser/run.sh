#!/bin/bash
# set -euo pipefail
#
# if [ ! -f ramdisk.igz ]; then
#     ./build.sh
# fi

exec qemu-system-x86_64 \
    -M q35 \
    -smp 2 \
    -m 2000M \
    -kernel kernel \
    -initrd new.igz \
    -append "root=/dev/ram0 migrate start=--headless" \
    -fw_cfg name=opt/org.toaruos.gettyargs,string="-a local /dev/ttyS0 115200" \
    -fw_cfg name=opt/org.toaruos.bootmode,string=headless \
		-no-reboot \
    -nographic
