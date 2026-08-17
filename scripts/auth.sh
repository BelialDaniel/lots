#!/bin/bash

set -e

cd /opt/auth

if [ ! -f "package.json" ]; then
    echo "creating Node app"
    pnpm init -y
    pnpm add --allow-build=esbuild \
        express@5.2.1 \
        drizzle-orm@0.45.2 \
        postgres@3.4.9 \
        dotenv@17.4.2 \
        jose@6.2.9 \
        @node-rs/argon2@2.1.0 \
        @scalar/express-api-reference@0.10.14 \
        zod@4.4.3
    pnpm add -D --allow-build=esbuild \
        drizzle-kit@0.31.10 \
        typescript@7.0.2 \
        tsx@4.23.12 \
        @types/express@5.0.6 \
        @types/node@26.2.0
fi

pnpm install --package-import-method=copy
exec pnpm start:dev
