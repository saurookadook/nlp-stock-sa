#!/usr/bin/env bash

set -e

if sudo security find-certificate -c nlp-ssa.dev > /dev/null 2>&1; then
  echo "Removing old certificate for 'nlp-ssa.dev' from system keychain..."
  sudo security delete-certificate -c nlp-ssa.dev
fi

echo "Generating wildcard SSL certificate for 'nlp-ssa.dev'..."
openssl req \
  -config nginx-reverse-proxy/config/openssl.conf \
  -new \
  -sha256 \
  -newkey rsa:2048 \
  -nodes \
  -x509 \
  -days 1825 \
  -keyout nginx-reverse-proxy/certs/nlp-ssa.dev.key \
  -out nginx-reverse-proxy/certs/nlp-ssa.dev.crt

echo "Adding trusted certificate for 'nlp-ssa.dev' to system keychain..."
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain nginx-reverse-proxy/certs/nlp-ssa.dev.crt
echo "Bingo bango! You're all set :]"
