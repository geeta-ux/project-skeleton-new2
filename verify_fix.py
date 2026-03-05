from apps.assessment_app.models import CareerAssessment
from apps.assessment_app.ai_utils import AICareerService
import json

a = CareerAssessment.objects.latest('id')
print(f"Assessment ID: {a.id}")
print(f"Old Scores: {a.scores}")

new_scores = AICareerService.calculate_scores(a.questions_data, a.answers_data)
print(f"New Scores: {new_scores}")

if new_scores['total'] > 0:
    print("SUCCESS: Scoring logic fixed!")
    # Optionally update the DB for this one record
    a.scores = new_scores
    a.save()
    print("Record updated.")
else:
    print("FAILURE: Scores still 0. Need further investigation.")
