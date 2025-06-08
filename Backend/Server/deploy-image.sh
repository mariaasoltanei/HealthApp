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

docker build -t worker1-test .
docker tag worker1-test 192.168.56.11:5001/worker1-test:latest
docker push 192.168.56.11:5001/worker1-test:latest
docker service update --force mystack_worker1

docker build -t worker2-test .
docker tag worker2-test 192.168.56.11:5001/worker2-test:latest
docker push 192.168.56.11:5001/worker2-test:latest
docker service update --force mystack_worker2

docker build -t worker3-test .
docker tag worker3-test 192.168.56.11:5001/worker3-test:latest
docker push 192.168.56.11:5001/worker3-test:latest
docker service update --force mystack_worker3

docker build -t manager-test .
docker tag manager-test 192.168.56.11:5001/manager-test:latest
docker push 192.168.56.11:5001/manager-test:latest
docker service update --force mystack_manager

docker tag nginx-proxy 192.168.56.11:5001/nginx-proxy:latest
docker push 192.168.56.11:5001/nginx-proxy:latest
docker service update --force mystack_nginx
