import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psychometric_project.settings')
django.setup()

from learning.models import Topic, PageContent

def seed():
    # 1. Verbal Reasoning
    verbal, created = Topic.objects.get_or_create(
        slug='verbal',
        defaults={
            'title': 'Verbal Reasoning',
            'description': 'Understand how to analyze written information, evaluate arguments, and draw conclusions.'
        }
    )
    if created:
        print("Created Verbal Reasoning Topic")
        # Add some sample content if needed, though for now the view renders static templates if we revert, 
        # BUT my view logic now relies on the DB for the context. 
        # Actually, looking at my view code:
        # def verbal_view(request):
        #    context = get_topic_content('verbal')
        #    return render(request, 'learning/verbal.html', context)
        # 
        # And the template `verbal.html` mostly has static text I wrote earlier. 
        # It DOES NOT strictly depend on `topic.contents` to render the *main* text I wrote in HTML.
        # However, `get_object_or_404` forces the Topic to exist.
    
    # 2. Personality
    personality, created = Topic.objects.get_or_create(
        slug='personality',
        defaults={
            'title': 'Personality Tests',
            'description': 'Discover how your traits and preferences align with different career paths and roles.'
        }
    )
    if created:
        print("Created Personality Topic")

    # 3. SJT
    sjt, created = Topic.objects.get_or_create(
        slug='sjt',
        defaults={
            'title': 'Situational Judgment Tests',
            'description': 'Learn to navigate workplace scenarios and demonstrate effective decision-making.'
        }
    )
    if created:
        print("Created SJT Topic")

if __name__ == '__main__':
    seed()
