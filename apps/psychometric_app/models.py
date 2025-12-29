from django.db import models
from apps.users_app.models import User

class PsychometricQuestion(models.Model):
    CATEGORY_CHOICES = [
        ('personality', 'Personality'),
        ('interest', 'Interest'),
        ('values', 'Values'),
    ]

    section = models.CharField(max_length=100)     # e.g., "psychometric"
    text = models.TextField()
    options = models.JSONField()                   # store Likert options
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )
    weight = models.FloatField(default=1.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'psychometric_questions'

    def __str__(self):
        return f"{self.category or self.section} - {self.text[:50]}"

class PsychometricSession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('standalone', 'Standalone'),
        ('full', 'Full Assessment'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='psychometric_sessions'
    )

    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES
    )

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'psychometric_sessions'

    def __str__(self):
        return f"{self.user} - {self.session_type}"

class PsychometricResponse(models.Model):
    session = models.ForeignKey(
        PsychometricSession,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    question = models.ForeignKey(
        PsychometricQuestion,
        on_delete=models.CASCADE
    )
    selected_option = models.CharField(max_length=100)
    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'psychometric_responses'
        unique_together = ('session', 'question')


class PsychometricResult(models.Model):
    session = models.OneToOneField(
        PsychometricSession,
        on_delete=models.CASCADE,
        related_name='result'
    )

    personality_score = models.IntegerField()
    interest_score = models.IntegerField()
    values_score = models.IntegerField()

    personality_percentile = models.IntegerField()
    interest_percentile = models.IntegerField()
    values_percentile = models.IntegerField()

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'psychometric_results'

    def __str__(self):
        return f"Result - {self.session.user}"

