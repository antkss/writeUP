#!/bin/esh

echo -n "Mounting tmpfs..." > /dev/pex/splash
mount tmpfs tmp,777 /tmp
mount tmpfs var,755 /var
mkdir /var/run
