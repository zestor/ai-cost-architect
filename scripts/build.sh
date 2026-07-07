#!/usr/bin/env bash
# Build the frontend and start the backend (which will also serve dist/)
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Building frontend …"
( cd "$DIR/frontend" && npm ci && npm run build )

echo "Starting production backend on :8765 (serves API + built frontend) …"
( cd "$DIR/backend" && python -m uvicorn main:app --host 0.0.0.0 --port 8765 )
