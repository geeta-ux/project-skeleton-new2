from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Topic
from .ai_service import AIService

def hub_view(request):
    topics = Topic.objects.all()
    # Fallback if no topics exist yet
    if not topics.exists():
        # Ideally we would seed this, but for now we handle empty state in template or logic
        pass 
    return render(request, 'learning/hub.html', {'topics': topics})

def get_topic_content(slug):
    topic = get_object_or_404(Topic, slug=slug)
    # Group contents by section headers if needed, or just pass all contents
    contents = topic.contents.all()
    return {'topic': topic, 'contents': contents}

def verbal_view(request):
    context = get_topic_content('verbal')
    return render(request, 'learning/verbal.html', context)

def personality_view(request):
    context = get_topic_content('personality')
    return render(request, 'learning/personality.html', context)

def sjt_view(request):
    context = get_topic_content('sjt')
    return render(request, 'learning/sjt.html', context)

@csrf_exempt
def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            topic_slug = data.get('topic', 'general')
            response = AIService.get_chat_response(topic_slug, message)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def generate_question_view(request):
    topic_slug = request.GET.get('topic')
    if not topic_slug:
         return JsonResponse({'error': 'Missing topic'}, status=400)
    
    questions = AIService.generate_question(topic_slug)
    if questions:
        # Wrap in a dict for consistency, or just return list. 
        # Returning dict {questions: []} is safer/cleaner.
        return JsonResponse({'questions': questions})
    return JsonResponse({'error': 'Could not generate questions'}, status=500)

@csrf_exempt
def career_advice_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic')
            user_data = data.get('performance_data')
            
            recommendations = AIService.get_career_advice(topic, user_data)
            return JsonResponse({'careers': recommendations})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
