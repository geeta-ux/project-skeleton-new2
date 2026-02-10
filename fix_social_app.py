from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Check all sites
print("\n=== All Sites in Database ===")
all_sites = Site.objects.all()
for site in all_sites:
    print(f"  Site ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print(f"\n=== Current Site (SITE_ID=1) ===")
try:
    current_site = Site.objects.get(id=1)
    print(f"  Domain: {current_site.domain}, Name: {current_site.name}")
except Site.DoesNotExist:
    print("  ❌ Site with ID=1 not found!")

print("\n=== Google OAuth Apps ===")
google_apps = SocialApp.objects.filter(provider='google')
print(f"Found {google_apps.count()} Google app(s):")

for app in google_apps:
    sites = list(app.sites.all())
    print(f"\n  App ID: {app.id}, Name: {app.name}")
    print(f"  Client ID: {app.client_id[:30]}...")
    print(f"  Linked to sites: {[f'{s.id}:{s.domain}' for s in sites]}")

# Fix: Update the site to localhost and link the app
print("\n=== Fixing Configuration ===")

# Update site 1 to localhost
site = Site.objects.get(id=1)
if site.domain != '127.0.0.1:8000':
    print(f"  Updating site domain from '{site.domain}' to '127.0.0.1:8000'")
    site.domain = '127.0.0.1:8000'
    site.name = 'CareerGuide Local'
    site.save()
    print("  ✅ Site updated")
else:
    print(f"  ✅ Site already set to '{site.domain}'")

# Ensure Google app is linked to site 1
if google_apps.exists():
    app = google_apps.first()
    if site not in app.sites.all():
        print(f"  Linking Google app to site '{site.domain}'...")
        app.sites.clear()  # Clear all sites first
        app.sites.add(site)
        print("  ✅ Google app linked to current site")
    else:
        print(f"  ✅ Google app already linked to '{site.domain}'")
        
    # Double-check for duplicates after clearing
    app.sites.clear()
    app.sites.add(site)
    print("  ✅ Ensured single site linkage")

print("\n=== Final Check ===")
google_apps = SocialApp.objects.filter(provider='google')
for app in google_apps:
    sites = list(app.sites.all())
    print(f"  App ID {app.id} linked to: {[f'{s.id}:{s.domain}' for s in sites]}")
