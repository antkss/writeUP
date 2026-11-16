# see compose.yml

FROM debian:bookworm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libarchive-tools  \
        qemu-system-x86 \
        ca-certificates wget pwgen && \
    rm -rf /var/lib/apt/lists

RUN useradd --create-home --shell /bin/bash ctf

COPY ynetd /sbin/
COPY run.sh /home/ctf

WORKDIR /root
COPY flag.txt build.sh image.iso /root/
RUN /root/build.sh && \
    mv kernel ramdisk.igz /home/ctf/ && \
    rm -r *

RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd && \
    chmod 004 /home/ctf/kernel /home/ctf/ramdisk.igz && \
    chmod 005 /home/ctf/run.sh

RUN ynetd -v

RUN find / -ignore_readdir_race -path /sys -prune -o -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -exec rm {} \;
USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root


WORKDIR /home/ctf
EXPOSE 1024
CMD /sbin/ynetd -pow 28 -lm 2147483648 -lt 30 -t 300 -sh n /home/ctf/run.sh
