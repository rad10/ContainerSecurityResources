#!/bin/bash

# docker-compose exec db bash /docker-entrypoint-init.d/06_backdoor.sh
echo exit | podman-compose exec empire /empire/ps-empire client -r empire.conf
sleep 2
podman-compose exec empire bash /empire/agent.sh
