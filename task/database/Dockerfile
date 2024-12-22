FROM ubuntu:24.04 AS base

FROM disconnect3d/nsjail

COPY --from=base / /jail/

COPY database /jail/database
COPY flag /jail/flag

COPY start.sh /start.sh
RUN chmod +x /start.sh
EXPOSE 18439

CMD [ "/start.sh" ]
