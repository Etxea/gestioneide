#!/bin/bash
source ./bin/activate
./manage.py runserver 9000
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program ./manage.py runserver 0.0.0.0:9000
