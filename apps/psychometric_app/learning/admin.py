from django.contrib import admin
from .models import Topic, PageContent, ScreeningDomain, ScreeningQuestion, ScreeningSession, ScreeningResponse


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


# --- Screening Models ---

@admin.register(ScreeningDomain)
class ScreeningDomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(ScreeningQuestion)
class ScreeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'text', 'domain')
    list_filter = ('domain',)
    search_fields = ('text',)


@admin.register(ScreeningSession)
class ScreeningSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'risk_level', 'is_completed')
    list_filter = ('risk_level', 'is_completed')
    readonly_fields = ('timestamp', 'domain_scores')


@admin.register(ScreeningResponse)
class ScreeningResponseAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'selected_choice', 'score')
    list_filter = ('selected_choice', 'score')