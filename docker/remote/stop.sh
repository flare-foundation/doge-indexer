#!/usr/bin/env bash
set -e

if [ -x "beforestop.sh" ]; then
	./beforestop.sh
fi

docker compose down
