#!/usr/bin/env bash
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" && cd "$CWD"

export SERVER_URL="http://localhost:8000"
SERVER_PID=0

function finish {
  ((SERVER_PID > 0)) && kill -15 $SERVER_PID
}
trap finish EXIT INT

fastapi dev server.py &
SERVER_PID=$!
sleep 3

PYTHONPATH=$PWD/.. python3 test.py
