import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_guide.settings')
django.setup()

from apps.assessment_app.models import CareerAssessment

assessments = CareerAssessment.objects.all().order_by('-id')[:5]
for a in assessments:
    print(f"ID: {a.id}, User: {a.user.email}")
    print(f"Questions Data Type: {type(a.questions_data)}")
    if a.questions_data:
        first_q = a.questions_data[0]
        print(f"First Question: {first_q.get('text')}")
        print(f"Options: {first_q.get('options')}")
        print(f"Options Type: {type(first_q.get('options'))}")
    print("-" * 20)
