#!/usr/bin/env bash
set -ex
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR/../.. && CWD=$PWD # move to project root

docker run --rm -it -v $PWD:/io -w /io ./res/postgres/test_docker.sh
