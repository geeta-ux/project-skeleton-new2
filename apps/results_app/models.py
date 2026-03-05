from django.db import models
from apps.users_app.models import User
from apps.assessment_app.models import CareerAssessment

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    assessment = models.OneToOneField(CareerAssessment, on_delete=models.CASCADE, null=True, blank=True, related_name='result')
    scores = models.JSONField(blank=True, null=True)
    primary_track = models.CharField(max_length=100, blank=True, null=True)
    secondary_track = models.CharField(max_length=100, blank=True, null=True)
    score_breakdown = models.JSONField(null=True, blank=True)  # JSONField
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'results'

class Plan(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='plans')
    year = models.IntegerField(default=1)  # add this
    plan_json = models.JSONField()


    class Meta:
        db_table = 'plans'
