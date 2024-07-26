#!/usr/bin/env bash
set -ex
apt update
apt-get install -y bash-completion postgresql postgresql-contrib libpq-dev \
                python3-pip python3.11-venv sudo

cd /root
[ ! -f .venv/bin/activate ] && python3 -m venv .venv && echo ". .venv/bin/activate" >> ~/.bashrc
. .venv/bin/activate
pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn psycopg2-binary sqlalchemy

service postgresql restart

cd /
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'banarama';"
sudo -u postgres psql -U postgres -c 'CREATE DATABASE collab;'

cd /root
python3 test_conn.py
alembic init migrations
sed -i 's#driver://user:pass@localhost/dbname#postgresql+psycopg2://postgres:banarama@0.0.0.0:5432/collab#g' alembic.ini
cp env.py migrations/env.py # overwrite default
alembic revision --autogenerate -m "Create a baseline migrations" && alembic upgrade head
python3 test_db.py
