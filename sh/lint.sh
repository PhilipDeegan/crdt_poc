#!/usr/bin/env bash
CWD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" && cd "$CWD/.."

set -e

(
  export PYTHONPATH=$PWD
  python3 -m black sciqlop test
  ruff check sciqlop test
  pylint --errors-only sciqlop test
  isort phlop sciqlop test
  PY_FILES=$(find sciqlop test -name "*.py")
  for FILE in ${PY_FILES[@]}; do
    autoflake -i "$FILE"
  done
)
