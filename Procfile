web: PYTHONPATH=$PYTHONPATH:$PWD/turkers NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn turkers.wsgi
release: python turkers/manage.py migrate --no-input;
