FROM docker.io/library/mysql:debian

# Add netcat to image
RUN apt update \
 && apt install -y ncat iputils-ping \
 && rm -rf /var/lib/apt/lists/*

# Add new start entrypoint adding additional ops
COPY start.sh /start.sh

ENTRYPOINT [ "/start.sh" ]
CMD [ "mysqld" ]
