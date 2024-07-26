#!/usr/bin/env bash
set -ex
apt update
apt-get install -y bash-completion postgresql postgresql-contrib libpq-dev \
                python3-pip python3.11-venv sudo

cd /root
[ ! -f .venv/bin/activate ] && python3 -m venv .venv
. .venv/bin/activate
pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn psycopg2-binary sqlalchemy

service postgresql restart

(
  cd /
  sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'banarama';"
  sudo -u postgres psql -U postgres -c 'CREATE DATABASE collab;'
)
