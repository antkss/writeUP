FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y socat git make cmake curl && \
	apt-get clean sudo gdb neovim tmux python3-pip
RUN mkdir /app && useradd user

ADD share/ /app/

RUN cd /tmp && \
	git clone https://github.com/DaveGamble/cJSON && \
	cd cJSON && \
	mkdir build && \
	cd build && \
	cmake .. && \
	make && \
	make install && \
	ldconfig
#RUN echo "user ALL=(ALL:ALL) ALL >>/etc/sudoers"
RUN chmod +x /app/* && \
	chmod 444 /app/flag.txt

USER root
WORKDIR /app
WORKDIR /app/pwndbg
RUN bash setup.sh
WORKDIR /app
COPY .gdbinit /root/.gdbinit

EXPOSE 9001

CMD ["/app/run.sh"]
