import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Set up Google OAuth Social Application'

    def handle(self, *args, **options):
        # Get credentials from environment
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('[ERROR] GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in environment'))
            return

        # Get or create the site
        site = Site.objects.get(pk=1)
        self.stdout.write(f'[INFO] Using site: {site.domain}')

        # Check if Google app already exists
        google_app = SocialApp.objects.filter(provider='google').first()

        if google_app:
            # Update existing app
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Updated existing Google OAuth app'))
        else:
            # Create new app
            google_app = SocialApp.objects.create(
                provider='google',
                name='Google',
                client_id=client_id,
                secret=client_secret,
            )
            google_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Created new Google OAuth app'))

        self.stdout.write(self.style.SUCCESS(f'[INFO] Client ID: {client_id[:20]}...'))
        self.stdout.write(self.style.SUCCESS('[SUCCESS] Google OAuth is now configured!'))
