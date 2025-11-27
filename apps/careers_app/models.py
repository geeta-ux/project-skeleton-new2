from django.db import models

class Career(models.Model):
    title = models.CharField(max_length=150)
    track = models.CharField(max_length=100, blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avg_salary_range = models.CharField(max_length=100, blank=True, null=True)
    sample_roles = models.JSONField(blank=True, null=True)
    class Meta:
        db_table = 'careers'

class CareerKB(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='kb_entries')
    title = models.CharField(max_length=150)
    content = models.TextField()
    tags = models.JSONField(blank=True, null=True)
    class Meta:
        db_table = 'career_kb'
