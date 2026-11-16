FROM ubuntu

RUN apt-get update
RUN apt-get install -y build-essential autoconf automake bison flex re2c gdb
RUN apt-get install -y libtool make pkgconf valgrind git libxml2-dev libsqlite3-dev nginx gdbserver neovim

WORKDIR /app

RUN git clone https://github.com/php/php-src.git
RUN cd php-src && git checkout php-8.4.0beta5

RUN cd php-src && ./buildconf --force && ./configure --enable-debug --prefix=/app/php-bin/DEBUG --with-config-file-path=/app/php-bin/DEBUG/etc --enable-fpm --with-fpm-user=ctf --with-fpm-group=ctf && make -j4 && make install

COPY php.ini /tmp

RUN cd /app/php-bin/DEBUG/etc && mv /tmp/php.ini . && mv php-fpm.d/www.conf.default php-fpm.d/www.conf && mv /app/php-bin/DEBUG/etc/php-fpm.conf.default php-fpm.conf && echo 'pm.max_requests = 1' >> php-fpm.d/www.conf

COPY juice.so /tmp
RUN cd /app/php-bin/DEBUG/lib/php/extensions/debug-non-zts-20230901 && mv /tmp/juice.so .

WORKDIR /app/source
COPY index.php .

COPY default /tmp
RUN cd /etc/nginx/sites-available/ && mv /tmp/default .

COPY hook.sh /tmp
RUN cd /app && mv /tmp/hook.sh .

RUN useradd -m ctf
EXPOSE 6969
EXPOSE 5002

CMD /app/hook.sh

