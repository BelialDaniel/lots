#!/bin/sh

set -e

# cd /opt/ui_toka
pnpm install --package-import-method=copy
exec pnpm dev --host 0.0.0.0
