FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat
RUN useradd -UM amnesia

COPY amnesia /home/amnesia/amnesia
COPY flag.txt /home/amnesia/flag.txt
COPY run.sh /home/amnesia/run.sh
RUN chown amnesia:amnesia /home/amnesia/flag.txt && chmod 644 /home/amnesia/flag.txt
USER amnesia

WORKDIR /home/amnesia
EXPOSE 20037
CMD /home/amnesia/run.sh
