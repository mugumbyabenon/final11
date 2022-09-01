
web: gunicorn --chdir libapp libapp.wsgi
celeryworker:celery -A libapp.celery worker & celery -A libapp beat --pool=solo -l INFO & wait -n
