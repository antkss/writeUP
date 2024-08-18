#!/bin/bash
killall boat;
cp * /tmp
cd /tmp

chmod 777 flag.txt

python3 chall-setup.py > /dev/null
chmod +x /tmp/boat
/tmp/boat 1032 
/tmp/boat 1033 
/tmp/boat 1035 
# /tmp/boat 1024 &
# /tmp/boat 1031
