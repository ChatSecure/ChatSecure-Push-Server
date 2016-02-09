worker: cd push && celery -A push.celery worker --loglevel=info
web: gunicorn --pythonpath=./push push.wsgi:application
