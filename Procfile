migrate: python -c "from ilikedthis.db.manager import setup_database; setup_database()"
web: gunicorn -b 0.0.0.0:$PORT ilikedthis.wsgi:app
