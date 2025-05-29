#!/bin/bash

FLASK_DIR="../Backend/Server"


NODES=(node1)

VAGRANT_CMD="/usr/local/bin/vagrant"
FLASK_FILE="test.py"
REMOTE_DIR="/home/vagrant/Server"


for NODE in "${NODES[@]}"; do
    echo "Copying Flask server to $NODE..."
    sudo $VAGRANT_CMD scp "$FLASK_DIR" "$NODE:/home/vagrant/"
    if [ $? -eq 0 ]; then
        echo "Successfully copied to $NODE"
    else
        echo "Failed to copy to $NODE"
    fi
done
