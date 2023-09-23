#!/bin/bash

set -m

# Give DB time to start up
sleep 3

# Starting empire
./ps-empire $@ &

# Sleep 5 seconds to let empire start up
sleep 5

# Start the agent
./agent.sh



fg %1