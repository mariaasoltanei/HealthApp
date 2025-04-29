#!/bin/bash

# Default empty
INSTANCE=""

# Parse input arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -instance) INSTANCE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$INSTANCE" ]; then
    echo "Error: You must specify an instance using -instance (e.g., manager, worker1, worker2, worker3)"
    exit 1
fi

cd ${INSTANCE}-service
ls
echo "Building Docker image for $INSTANCE..."
docker build -t ${INSTANCE}-test .

echo "Tagging image for private registry..."
docker tag ${INSTANCE}-test 192.168.56.11:5001/${INSTANCE}-test:latest

echo "Pushing image to private registry..."
docker push 192.168.56.11:5001/${INSTANCE}-test:latest

echo "Forcing update of Swarm service mystack_${INSTANCE}..."
docker service update --force mystack_${INSTANCE}
cd ..
echo "✅ Deployment for $INSTANCE completed!"
