#!/bin/bash

FLASK_DIR="../Backend/Server"


NODES=(node1 node2 node3 node4)

VAGRANT_CMD="/usr/local/bin/vagrant"
FLASK_FILE="test.py"
REMOTE_DIR="/home/vagrant/Server"

# for NODE in "${NODES[@]}"; do
#   echo "➡️  $NODE: Starting Flask app..."
#   sudo $VAGRANT_CMD ssh "$NODE" -c "cd $REMOTE_DIR && nohup python3 $FLASK_FILE > flask.log 2>&1 &"
#   if [ $? -eq 0 ]; then
#     echo "✅ $NODE: Flask started"
#   else
#     echo "❌ $NODE: Failed to start Flask"
#   fi
# done


for NODE in "${NODES[@]}"; do
    echo "Copying Flask server to $NODE..."
    sudo $VAGRANT_CMD scp "$FLASK_DIR" "$NODE:/home/vagrant/"
    if [ $? -eq 0 ]; then
        echo "Successfully copied to $NODE"
    else
        echo "Failed to copy to $NODE"
    fi
done

