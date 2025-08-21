#!/usr/bin/env bash

set -e

KEY_FILE="nginx-reverse-proxy/certs/nlp-ssa.dev+4-key.pem"
PEM_FILE="nginx-reverse-proxy/certs/nlp-ssa.dev+4.pem"

if [[ -f "$KEY_FILE" && -f "$PEM_FILE" ]]; then
    echo "✅ Certs for 'nlp-ssa.dev' already exist!"
else
    echo "⏳ Creating certs for 'nlp-ssa.dev'..."
    cd nginx-reverse-proxy/certs
    mkcert nlp-ssa.dev "*.nlp-ssa.dev" localhost 127.0.0.1 ::1
    # NOTE: files created from the above command should be
    # - nlp-ssa.dev+4-key.pem
    # - nlp-ssa.dev+4.pem
    echo "✅ Certs for 'nlp-ssa.dev' successfully created!"
    cd ../..
fi

# Define the line we want to check/append
LINE='127.0.0.1 nlp-ssa.dev *.nlp-ssa.dev database'
HOSTS_FILE='/etc/hosts'

# Check if the line exists exactly as is
# NOTES
# - `grep -Fxq`:
#   `-F`: fixed string match (not regex)
#   `-x`: match the whole line exactly
#   `-q`: quiet, no output, exit status only
if grep -Fxq "$LINE" "$HOSTS_FILE"; then
    echo "✅ Entry already exists in $HOSTS_FILE."
else
    echo "⏳ Entry not found. Appending it to $HOSTS_FILE..."
    # NOTES:
    # - `sudo` is used for appending because modifying `/etc/hosts` usually requires root permission.
    # - `tee -a` is used instead of direct redirection (`>>`) to  play nice with `sudo`
    echo "$LINE" | sudo tee -a "$HOSTS_FILE" > /dev/null
    echo "✅ Entry appended successfully."
fi

echo "🚀 Bingo bango! You're all set :] 🚀"


