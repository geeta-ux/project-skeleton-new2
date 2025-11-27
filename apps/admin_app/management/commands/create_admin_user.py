# from doctest import example
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from apps.admin_app import admin

User = get_user_model()

class Command(BaseCommand):
    help = "Creates a default admin user"

    def handle(self, *args, **options):
        admin_email = "admin@example.com"

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(email=admin_email,password="admin123",name="Admin",)
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write("Admin user already exists")
