#!/bin/bash
cp * /tmp
cd /tmp

# chmod 777 flag.txt

python3 chall-setup.py > /dev/null
chmod +x /tmp/boat
./boat 1032 | ./boat 1033 | ./boat 1035 | ./boat 1024 | ./boat 1031
# LD_PRELOAD="/tmp/libcrypto.so.3/tmp/libc.so.6" /tmp/boat 1031
