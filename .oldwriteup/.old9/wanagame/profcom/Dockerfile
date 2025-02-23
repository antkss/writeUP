FROM ubuntu:24.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing -y && apt-get -y upgrade
RUN apt-get install -y ncat 

RUN useradd -m ctf


RUN chown -R ctf:ctf /home/ctf/
COPY pro /home/ctf
COPY flag /home/ctf
RUN chmod +x /home/ctf/pro
RUN chmod 400 /home/ctf/flag

WORKDIR /home/ctf
EXPOSE 3737
CMD ["ncat", "-lnvp", "3737", "-e", "/home/ctf/pro", "-k"]
