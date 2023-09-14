#!/usr/bin/env bash
set -e

if [ -f ".disable-deploy" ]; then
	echo "Automatic deploy disabled"
	exit 1
fi

if [ -x "beforedeploy.sh" ]; then
	./beforedeploy.sh
fi

docker compose pull
docker compose up -d
