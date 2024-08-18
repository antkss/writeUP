FROM ubuntu:22.04
RUN apt update && apt install -y socat
WORKDIR /challenge
COPY pacipac pacipac
EXPOSE 1337
RUN useradd --user-group --system --create-home --no-log-init ctf
COPY flag.txt flag.txt
USER ctf
ENTRYPOINT ["socat", "tcp-l:1337,reuseaddr,fork", "EXEC:/challenge/pacipac"]
