#!/bin/bash

FLASK_DIR="../Backend/Server"


NODES=(node1 node2 node3 node4)

VAGRANT_CMD="/usr/local/bin/vagrant"
FLASK_FILE="test.py"
REMOTE_DIR="/home/vagrant/Server"

REGISTRY_IP="192.168.56.11"  # node1 IP
REGISTRY_PORT="5000"
IMAGE_NAME="flask-sensor-app"
TAG="latest"
FULL_IMAGE="${REGISTRY_IP}:${REGISTRY_PORT}/${IMAGE_NAME}:${TAG}"
NODES=(node1 node2 node3 node4)

echo "🧰 Setting up local Docker registry on node1..."

# Start the registry container on node1
sudo $VAGRANT_CMD ssh node1 -c "docker ps | grep registry || docker run -d -p ${REGISTRY_PORT}:5000 --restart=always --name registry registry:2"

echo "🐳 Building and pushing Docker image on node1..."
sudo $VAGRANT_CMD ssh node1 -c "
  cd /home/vagrant/Server &&
  docker build -t ${FULL_IMAGE} . &&
  docker push ${FULL_IMAGE}
"

echo "🔐 Configuring Docker daemons to allow insecure registry on all nodes..."

# Configure each node to trust the local registry
for NODE in "${NODES[@]}"; do
  echo "⚙️  $NODE: Updating Docker daemon.json"
  sudo $VAGRANT_CMD ssh "$NODE" -c "
    echo '{\"insecure-registries\": [\"${REGISTRY_IP}:${REGISTRY_PORT}\"]}' | sudo tee /etc/docker/daemon.json > /dev/null &&
    sudo systemctl restart docker
  "
done

echo "📥 Pulling image from registry on all nodes..."
for NODE in "${NODES[@]}"; do
  echo "⬇️  $NODE: Pulling image..."
  sudo $VAGRANT_CMD ssh "$NODE" -c "docker pull ${FULL_IMAGE}"
done

echo "✅ Local registry setup complete and image is available on all nodes."
