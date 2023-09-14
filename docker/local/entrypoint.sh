#!/usr/bin/env bash

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" 2>/dev/null; do
	echo "waiting for postgres"
	sleep 1
done

# python manage.py collectstatic --no-input --settings=${DJANGO_SETTINGS_MODULE}
# python manage.py migrate --settings=${DJANGO_SETTINGS_MODULE}

[ -z ${ADMIN_EMAIL+x} ] | [ -z ${ADMIN_PASSWORD+x} ] || python manage.py admin_user --email $ADMIN_EMAIL --password $ADMIN_PASSWORD --settings=${DJANGO_SETTINGS_MODULE}

exec python manage.py runserver "0.0.0.0:8000" --settings=${DJANGO_SETTINGS_MODULE}
