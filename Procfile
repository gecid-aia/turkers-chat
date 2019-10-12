web: gunicorn turkers.turkers.wsgi
release: python turkers/manage.py migrate --no-input; python turkers/manage.py clear_cache;
