from django.db import models
from apps.users_app.models import User

class Question(models.Model):
    section = models.CharField(max_length=100)
    text = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255, blank=True, null=True)
    weight = models.FloatField(default=1.0)
    class Meta:
        db_table = 'questions'

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessments')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'assessments'

class Response(models.Model):
    assessment = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        related_name='responses',
        # null=True,
        # blank=True
    )
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'responses'
