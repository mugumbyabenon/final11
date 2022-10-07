
web: gunicorn --chdir libapp libapp.wsgi
celeryworker:celery -A libapp.celery worker & celery -A libapp beat --pool=solo -l INFO & wait -n
celery: -A libapp.celery worker --pool=solo -l info
celerybeat: celery -A libapp beat -l info
