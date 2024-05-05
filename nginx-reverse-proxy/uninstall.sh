#!/usr/bin/env bash

set -e

if sudo security find-certificate -c nlp-ssa.dev > /dev/null 2>&1; then
  echo "Removing old certificate for 'nlp-ssa.dev' from system keychain..."
  sudo security delete-certificate -c nlp-ssa.dev
fi

echo "Removing DNS resolver for 'nlp-ssa.dev'..."
sudo rm -rf /etc/resolver/nlp-ssa.dev

echo "Destroying containers..."
docker-compose down -v --remove-orphans

echo "Done!"
