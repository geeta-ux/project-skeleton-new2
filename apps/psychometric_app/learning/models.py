from django.db import models
from django.conf import settings
from django.utils import timezone

class Topic(models.Model):
    TOPIC_CHOICES = [
        ('verbal', 'Verbal Reasoning'),
        ('personality', 'Personality Tests'),
        ('sjt', 'Situational Judgment Tests'),
    ]
    slug = models.SlugField(max_length=50, unique=True, choices=TOPIC_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField(help_text="Short description for the hub card")

    def __str__(self):
        return self.title

class PageContent(models.Model):
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('format', 'Format & Structure'),
        ('types', 'Question Types'),
        ('rules', 'Rules'),
        ('tips', 'Preparation Tips'),
        ('intro', 'Introduction/Concept'),
        ('scoring', 'Scoring'),
        ('examples', 'Examples'),
        ('categories', 'Categories'),
        ('differences', 'Differences'),
    ]
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='contents')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(help_text="HTML allowed")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.get_section_type_display()}"

# --- Screening Models ---

class ScreeningDomain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ScreeningQuestion(models.Model):
    text = models.TextField()
    domain = models.ForeignKey(ScreeningDomain, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    # Choice weights: A=0, B=1, C=2, D=3
    choice_a = models.CharField(max_length=200, default='Not at all')
    choice_b = models.CharField(max_length=200, default='Several days')
    choice_c = models.CharField(max_length=200, default='More than half the days')
    choice_d = models.CharField(max_length=200, default='Nearly every day')
    is_active = models.BooleanField(default=True)   # << add this

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}..."

class ScreeningSession(models.Model):
    RISK_LEVELS = [
        ('low', 'Low / Stable'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='low')
    domain_scores = models.JSONField(default=dict) # Store scores per domain: {"Mood": 5, "Anxiety": 2, ...}
    recommendation = models.TextField(blank=True, default='')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session for {self.user.email} at {self.timestamp}"

class ScreeningResponse(models.Model):
    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    session = models.ForeignKey(ScreeningSession, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE)
    selected_choice = models.CharField(max_length=1, choices=CHOICES)
    score = models.IntegerField() # 0 to 3

    class Meta:
        unique_together = ('session', 'question')
