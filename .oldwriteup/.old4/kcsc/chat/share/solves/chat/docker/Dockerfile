FROM ubuntu:24.04

RUN apt update && apt install -y && apt clean
RUN useradd ctf && mkdir /app

ADD share/ /app/

RUN chmod +x /app/* && chmod 444 /app/flag.txt

USER ctf
WORKDIR /app

CMD "/app/run.sh"


