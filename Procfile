web: gunicorn antique_shop1.wsgi --workers 2 --log-file -
release: python manage.py migrate && python create_admin.py