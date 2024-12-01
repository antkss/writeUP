FROM ubuntu:22.04 

RUN useradd -ms /bin/bash pwn
WORKDIR /home/pwn

COPY . /home/pwn
# ADD flag /home/pwn

RUN chmod 4 /home/pwn/flag
RUN chmod 5 /home/pwn/simulation

RUN apt-get update -y
RUN apt-get install socat gdb nmap -y
USER pwn

EXPOSE 2007

ENTRYPOINT ["sh", "-c", "exec socat -s TCP-LISTEN:2007,reuseaddr,fork EXEC:/home/pwn/simulation,stderr"]
