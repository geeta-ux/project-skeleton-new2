from django.core.management.base import BaseCommand
from apps.psychometric_app.learning.models import ScreeningDomain, ScreeningQuestion

class Command(BaseCommand):
    help = 'Seed the screening questions and domains'

    def handle(self, *args, **options):
        # 1. Create Domains
        domains_data = {
            'Mood': 'Low interest, sadness, emotional exhaustion, lack of motivation.',
            'Anxiety': 'Tension, worry, nervousness, overthinking.',
            'Sleep': 'Quality and consistency of rest.',
            'Cognition': 'Focus, decision-making, logical reliance.',
            'Emotional Regulation': 'Emotional control, regulation, fluctuation.',
            'Social Functioning': 'Connection to others, communication under pressure.',
            'Functional Capacity': 'Handling daily responsibilities, adapting to change, confidence.',
            'Duration': 'Time-based criteria for how long symptoms have persisted.'
        }

        domain_objs = {}
        for name, desc in domains_data.items():
            domain, created = ScreeningDomain.objects.get_or_create(name=name, defaults={'description': desc})
            domain_objs[name] = domain
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created domain: {name}'))

        # 2. Questions Data
        questions = [
            # Mood
            (1, "Over the past two weeks, how often have you felt little interest or pleasure in doing things?", 'Mood'),
            (6, "How often do you feel emotionally exhausted?", 'Mood'),
            (11, "How often do you feel mentally fatigued even after resting?", 'Mood'),
            (18, "How often do you feel motivated to start tasks that require effort?", 'Mood'),
            
            # Anxiety
            (2, "How often have you felt tense, nervous, or on edge?", 'Anxiety'),
            (3, "When faced with stress, what happens most often?", 'Anxiety'),
            (13, "How often do you find yourself overthinking decisions after they are made?", 'Anxiety'),
            
            # Sleep
            (4, "How would you describe your sleep recently?", 'Sleep'),
            
            # Cognition
            (5, "How easy is it for you to concentrate on tasks?", 'Cognition'),
            (20, "When faced with a difficult situation, what do you usually rely on most?", 'Cognition'),
            
            # Emotional Regulation
            (7, "How do you usually respond to strong emotions (anger, sadness, anxiety)?", 'Emotional Regulation'),
            (12, "When plans change unexpectedly, how do you usually react?", 'Emotional Regulation'),
            (15, "How often do strong emotions interfere with what you intend to do?", 'Emotional Regulation'),
            (19, "How would you describe your emotional state throughout a typical day?", 'Emotional Regulation'),
            
            # Social Functioning
            (8, "How connected do you feel to people around you?", 'Social Functioning'),
            (16, "When interacting with others under pressure, what happens most often?", 'Social Functioning'),
            
            # Functional Capacity
            (9, "How confident do you feel in handling daily responsibilities?", 'Functional Capacity'),
            (14, "How manageable do your daily responsibilities feel right now?", 'Functional Capacity'),
            (17, "How confident do you feel about handling unexpected challenges?", 'Functional Capacity'),
            
            # Duration
            (10, "How long have these experiences been affecting you?", 'Duration'),
        ]

        # Standard choices for most questions
        default_choices = {
            'choice_a': 'Not at all / Rarely / Well',
            'choice_b': 'Several days / Occasionally / Moderate',
            'choice_c': 'More than half the days / Often / Difficult',
            'choice_d': 'Nearly every day / Almost always / Very poor'
        }

        # Override choices for specific questions if needed (based on the user's list)
        question_choices = {
            1: ('Not at all', 'Several days', 'More than half the days', 'Nearly every day'),
            2: ('Rarely', 'Occasionally', 'Frequently', 'Almost constantly'),
            3: ('I stay calm and focused', 'I feel uneasy but manage', 'I feel overwhelmed', 'I shut down or avoid the situation'),
            4: ('Restful and consistent', 'Slightly disturbed', 'Frequently disrupted', 'Very poor or irregular'),
            5: ('Very easy', 'Slightly difficult', 'Difficult most of the time', 'Extremely difficult'),
            6: ('Almost never', 'Occasionally', 'Often', 'Almost every day'),
            7: ('I regulate them well', 'I need some time but recover', 'I feel emotionally overwhelmed', 'I feel out of control'),
            8: ('Very connected', 'Somewhat connected', 'Mostly disconnected', 'Completely disconnected'),
            9: ('Very confident', 'Moderately confident', 'Low confidence', 'Not confident at all'),
            10: ('Less than a week', 'A few weeks', 'Several months', 'More than six months'),
            11: ('Almost never', 'Occasionally', 'Often', 'Almost every day'),
            12: ('I adapt easily', 'I feel uncomfortable but adjust', 'I feel stressed and irritated', 'I feel overwhelmed or shut down'),
            13: ('Rarely', 'Sometimes', 'Frequently', 'Almost always'),
            14: ('Very manageable', 'Mostly manageable', 'Hard to manage', 'Unmanageable'),
            15: ('Almost never', 'Occasionally', 'Often', 'Almost always'),
            16: ('I communicate clearly', 'I hesitate or become cautious', 'I react emotionally', 'I withdraw or avoid interaction'),
            17: ('Very confident', 'Somewhat confident', 'Slightly confident', 'Not confident at all'),
            18: ('Almost always', 'Often', 'Sometimes', 'Rarely'),
            19: ('Mostly stable', 'Slightly fluctuating', 'Highly fluctuating', 'Unpredictable and intense'),
            20: ('Logical thinking', 'Past experience', 'Emotional instinct', 'Avoidance or delay'),
        }

        for order, text, domain_name in questions:
            choices = question_choices.get(order, (
                default_choices['choice_a'],
                default_choices['choice_b'],
                default_choices['choice_c'],
                default_choices['choice_d']
            ))
            
            q, created = ScreeningQuestion.objects.get_or_create(
                order=order,
                defaults={
                    'text': text,
                    'domain': domain_objs[domain_name],
                    'choice_a': choices[0],
                    'choice_b': choices[1],
                    'choice_c': choices[2],
                    'choice_d': choices[3],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created question {order}'))
            else:
                # Update if already exists to ensure correct domain and choices
                q.text = text
                q.domain = domain_objs[domain_name]
                q.choice_a = choices[0]
                q.choice_b = choices[1]
                q.choice_c = choices[2]
                q.choice_d = choices[3]
                q.save()
