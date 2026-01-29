import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psychometric_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'admin123'

try:
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.email = email
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"Superuser '{username}' updated successfully.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully.")
except Exception as e:
    print(f"Error: {e}")
