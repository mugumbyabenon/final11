
web: gunicorn --chdir libapp libapp.wsgi
celery: -A libapp.celery worker --pool=solo -l info
celerybeat: celery -A libapp beat -l info
celeryworker:celery -A libapp.celery worker & celery -A libapp beat --pool=solo -l INFO & wait -n
