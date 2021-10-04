#!/bin/bash
source ./bin/activate
if test -f newrelic.ini
then
	NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program ./manage.py runserver 0.0.0.0:9000
else

	./manage.py runserver 9000
fi
