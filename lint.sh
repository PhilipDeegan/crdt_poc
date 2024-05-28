#!/usr/bin/env bash
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" && cd "$CWD"

set -e

python3 -m black .
pylint --errors-only .
isort phlop .

PY_FILES=$(find . -name "*.py")
for FILE in ${PY_FILES[@]}; do
  autoflake -i "$FILE"
done
