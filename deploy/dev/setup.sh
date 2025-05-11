#!/usr/bin/env sh
set -e

echo "Installing mkcert"
sudo apt install -y mkcert libnss3-tools

echo "Generating mkcert CA ROOT"
mkcert -install

echo "Editing /etc/hosts"
if ! grep -q "app.open-mfa.local" /etc/hosts; then
    sudo sh -c "cat hosts >> /etc/hosts"
    echo "Hosts file updated"
else
    echo "Hosts already configured, skipping"
fi
echo "Setup finished"