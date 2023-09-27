FROM docker.io/bcsecurity/empire:v5.6.3

RUN apt update \
 && apt install -y ncat nano

COPY agent.sh agent.sh
COPY start.sh start.sh

ENTRYPOINT [ "./start.sh" ]
CMD [ "server" ]
