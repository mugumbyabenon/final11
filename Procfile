release: python manage.py migrate
web: gunicorn --chdir library library.wsgi
celery: -A libapp.celery worker --pool=solo -l info
celerybeat: celery -A libapp beat -l info