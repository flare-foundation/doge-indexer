#!/usr/bin/env bash

until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" 2>/dev/null; do
	echo "waiting for postgres"
	sleep 1
done

[ -z ${ADMIN_EMAIL+x} ] | [ -z ${ADMIN_PASSWORD+x} ] || python manage.py admin_user --email $ADMIN_EMAIL --password $ADMIN_PASSWORD --settings=${DJANGO_SETTINGS_MODULE}

python manage.py collectstatic --no-input --settings=${DJANGO_SETTINGS_MODULE}
python manage.py migrate --settings=${DJANGO_SETTINGS_MODULE}

exec uwsgi --chdir=/app --module=project.wsgi:application --env DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} --master --protocol=uwsgi --socket=0.0.0.0:3030 --enable-threads --processes=2
