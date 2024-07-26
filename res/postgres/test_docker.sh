#!/usr/bin/env bash
set -ex
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR/../.. && CWD=$PWD # move to project root

export PYTHONPATH=$PWD

service postgresql restart # to be sure

[[ -z "$VIRTUAL_ENV" ]] && . /root/.venv/bin/activate && python3 -m pip install -r requirements.txt

rm -rf tmp && mkdir -p tmp && cd tmp
alembic init migrations
sed -i 's#driver://user:pass@localhost/dbname#postgresql+psycopg2://postgres:banarama@0.0.0.0:5432/collab#g' alembic.ini
cp "$SCRIPT_DIR/env.py" migrations/env.py # overwrite default
alembic revision --autogenerate -m "Create a baseline migrations"
alembic upgrade head

(
  cd "$SCRIPT_DIR"
  python3 test_db.py
)
