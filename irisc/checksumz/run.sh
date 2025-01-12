#!/usr/bin/bash
make exploit;
cd /home/as/irisc/checksumz;
cd /home/as/irisc/checksumz/artifacts;
rm -r /home/as/irisc/checksumz/artifacts/root/*;
cd root;
mv ../initramfs.cpio.gz .; 
gzip -d initramfs.cpio.gz;
cpio -i < initramfs.cpio;
rm initramfs.cpio;
cp /home/as/irisc/checksumz/exploit/exploit .;
# cp /home/as/irisc/checksumz/gdbserver bin
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../../artifacts/initramfs.cpio.gz;
cd ..
rm -r /home/as/irisc/checksumz/artifacts/root/*
cd /home/as/irisc/checksumz/ 
./start.sh --debug


