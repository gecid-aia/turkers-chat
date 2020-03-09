web: PYTHONPATH=$PYTHONPATH:$PWD/turkers gunicorn turkers.wsgi
release: python turkers/manage.py migrate --no-input;
