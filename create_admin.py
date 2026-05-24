import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antique_shop1.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USERNAME', 'ispanochka')
password = os.environ.get('ADMIN_PASSWORD', '6978Qwarry')
email    = os.environ.get('ADMIN_EMAIL', 'Qwarry086@gmail.com')

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f'Admin "{username}" created successfully.')
else:
    print('Admin already exists or credentials not set.')