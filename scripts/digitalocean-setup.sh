#! /usr/bin/env sh

# Exit in case of error
set -e

# Install docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-cache policy docker-ce
apt-get install -y docker-ce
apt install -y apache2-utils

# Install compose
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Initialize app's variables
python3 app/initialize.py
mv .env app

# Get env vars
echo "Qual o domínio?"
read DOMAIN
echo "Qual o domínio da imagem?"
read IMAGE_DOMAIN
echo "Qual a tag da imagem?"
read TAG
echo "Qual seu email?"
read EMAIL
echo "Qual senha pro traefik?"
read PASS
htpasswd -nb admin "$PASS" > .htpasswd

DOMAIN=$DOMAIN \
    IMAGE_DOMAIN=$IMAGE_DOMAIN \
    TAG=$TAG \
    EMAIL=$EMAIL \
    HASHED_PASSWORD=$HASHED_PASSWORD \
    ./scripts/generate-stack.sh

# Get IP
IP=$(curl http://checkip.amazonaws.com)
# Initialize swarm
docker swarm init --advertise-addr $IP || true
# Create the proxy network
docker network create -d overlay --attachable proxy || true

# Create acme file
touch acme.json
chmod 600 acme.json

./scripts/deploy.sh
