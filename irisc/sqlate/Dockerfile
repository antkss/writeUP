FROM ubuntu:22.04

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update && apt install socat -y

COPY . /home/user/

# USER user
WORKDIR /home/user
EXPOSE 5000
CMD ["socat", "TCP-L:5000,fork,reuseaddr", "EXEC:'./vuln'"]
# CMD ["sh", "-c", "cd /home/user && /home/user/vuln"]

