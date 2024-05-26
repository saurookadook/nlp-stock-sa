#!/usr/bin/env bash

set -e

./nginx-reverse-proxy/generate-certs.sh

# Ensure /etc/resolver exists before usage
if [ ! -d /etc/resolver ]; then
  echo "Creating /etc/resolver..."
  sudo mkdir /etc/resolver
fi

# Add DNS resolver
if [ ! -f /etc/resolver/nlp-ssa.dev ]; then
  echo "Adding DNS resolver for 'nlp-ssa.dev'..."
  echo -e "nameserver 127.0.0.1\nport 53535\n" | sudo tee /etc/resolver/nlp-ssa.dev
fi

echo "Starting nlp-ssa-proxy and dnsmasq..."
# docker-compose up dnsmasq nginx --build -d
docker compose up nginx --build -d

echo "All done!"
echo "........."
echo "View all of your local sites here: https://nlp-ssa.dev"
