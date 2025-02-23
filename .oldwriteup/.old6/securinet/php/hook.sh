#!/bin/sh
# while true;do
echo $FLAG > /flag_$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 20 | head -n 1)
unset FLAG
echo "Challenge started."
service nginx start
gdbserver --multi :6969 /app/php-bin/DEBUG/sbin/php-fpm -c /app/php-bin/DEBUG/etc/php.ini --nodaemonize
# /app/php-bin/DEBUG/sbin/php-fpm -c /app/php-bin/DEBUG/etc/php.ini --nodaemonize
# done
