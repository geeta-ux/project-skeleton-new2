from django.contrib import admin
from .models import Topic, PageContent

class PageContentInline(admin.StackedInline):
    model = PageContent
    extra = 1

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    inlines = [PageContentInline]

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'section_type', 'title', 'order')
    list_filter = ('topic', 'section_type')
