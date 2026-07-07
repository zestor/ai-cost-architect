#!/usr/bin/env bash
# Start backend and frontend in dev mode (two terminals)
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Starting backend on :8765 …"
( cd "$DIR/backend" && python -m uvicorn main:app --host 0.0.0.0 --port 8765 --reload ) &
BACKEND_PID=$!

echo "Starting frontend on :5173 …"
( cd "$DIR/frontend" && npm run dev ) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
