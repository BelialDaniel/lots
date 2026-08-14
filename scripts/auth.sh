#!/bin/bash

if [ ! -f "pyproject.toml" ]; then
    echo "creating toml file"
    uv init .
    uv add "fastapi[standard]"
fi

uv sync

exec uv run fastapi dev main.py --host 0.0.0.0 --port 8000
