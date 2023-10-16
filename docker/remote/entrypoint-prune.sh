#!/usr/bin/env bash

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" 2>/dev/null; do
	echo "waiting for postgres"
	sleep 1
done

until nc -z appserver 3030 2>/dev/null; do
	echo "waiting for server"
	sleep 1
done

sleep 1

exec python -u manage.py block_pruning --settings=${DJANGO_SETTINGS_MODULE}
