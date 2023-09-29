#!/bin/bash

# docker-compose exec db bash /docker-entrypoint-init.d/06_backdoor.sh
echo exit | docker-compose exec empire /empire/ps-empire client -r empire.conf
