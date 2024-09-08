FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y socat git make cmake curl && \
	apt-get clean
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

RUN chmod +x /app/* && \
	chmod 444 /app/flag.txt

USER user
WORKDIR /app

CMD ["/app/run.sh"]