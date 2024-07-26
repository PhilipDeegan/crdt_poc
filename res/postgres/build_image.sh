#!/usr/bin/env bash
set -ex
FULL_NAME="sciqlop/collab/debian:latest"
docker build -t ${FULL_NAME} .
