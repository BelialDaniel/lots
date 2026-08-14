#!/bin/sh

set -e

cd /opt/ui

if [ ! -f "package.json" ]; then
    echo "creating React Router app"
    pnpm dlx create-react-router@latest . \
        --yes \
        --no-git-init \
        --no-install \
        --package-manager pnpm
fi

pnpm install --package-import-method=copy
exec pnpm dev --host 0.0.0.0
