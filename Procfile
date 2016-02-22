worker: cd push && celery -A push.celery worker --loglevel=debug --without-gossip --without-mingle --without-heartbeat
web: gunicorn --pythonpath=./push push.wsgi:application
