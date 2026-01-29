from django.db import models

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
