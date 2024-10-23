#!/bin/bash
[[ -z "$1" ]] && echo "Please provide a spotify track url" && exit 1
cd "$(dirname "$0")"
poetry run python cli.py $1