web: daphne project.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A project worker -l info
release: ./release.sh
