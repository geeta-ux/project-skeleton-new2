import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guide.settings')
django.setup()

from apps.assessment_app.models import CareerAssessment

# Get the absolute last assessment
a = CareerAssessment.objects.latest('id')
print(f"Assessment ID: {a.id}")
print(f"User: {a.user.email}")
print(f"Completed: {a.completed}")

# Print questions_data clearly
print("QUESTIONS DATA:")
print(json.dumps(a.questions_data[:2], indent=2)) # Just first 2
