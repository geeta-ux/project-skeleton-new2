import os
import json
import random
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AIContext:
    VERBAL_CONTEXT = """You are a psychometric assessment expert specializing in verbal reasoning tests.
    Generate a JSON object containing a list of 10 unique, high-quality verbal reasoning questions.
    The valid question types are: 'statement', 'reading_comp', 'sentence_completion', 'synonym'.
    
    Output Format:
    {
      "questions": [
        {
          "type": "statement",
          "text": "Passage: [text]... Statement: [text]",
          "options": ["True", "False", "Cannot Say"],
          "correct_index": 0,
          "explanation": "Reasoning...",
          "weight": 5
        }
      ]
    }
    Strictly return valid JSON."""

    PERSONALITY_CONTEXT = """You are a psychometric assessment expert.
    Generate a JSON object containing a list of 10 personality assessment items.
    Include a mix of Trait-Based (Likert) and Type-Based (Forced Choice) questions.
    
    Output Format:
    {
      "questions": [
        {
          "type": "trait_based",
          "trait": "Openness",
          "text": "Statement: I enjoy trying new foods.",
          "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
          "correct_index": -1,
          "weights": {"Strongly Disagree": 1, ...}
        }
      ]
    }
    Strictly return valid JSON."""

    SJT_CONTEXT = """You are an SJT expert.
    Generate a JSON object with 10 Situational Judgment Test scenarios.
    
    Output Format:
    {
      "questions": [
        {
          "competency": "Teamwork",
          "text": "Scenario: ...",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correct_index": 2,
          "explanation": "Why this is the best...",
          "scores": [1, 2, 5, 0],
          "qualities": ["Poor", "Acceptable", "Best", "Very Poor"]
        }
      ]
    }
    Strictly return valid JSON."""

    CAREER_CONTEXT = """You are a career counselor.
    Analyze the user's performance/preferences: {data}
    Topic: {topic}
    
    Task: Suggest 3 distinct career paths that fit this profile.
    If the data is insufficient, suggest 3 general careers suitable for someone interested in {topic}.
    
    REQUIRED Output Format (JSON):
    {{
      "careers": [
        {{
          "role": "Job Title",
          "reason": "Explanation...",
          "industry": "Industry"
        }}
      ]
    }}
    """

class AIService:
    @staticmethod
    def get_career_advice(topic, user_data):
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Ensure we don't pass too much empty data
            valid_data = [x for x in user_data if x]
            
            prompt = AIContext.CAREER_CONTEXT.format(topic=topic, data=json.dumps(valid_data))
            
            response = model.generate_content(prompt)
            print(f"DEBUG: Gemini Response: {response.text}")
            
            # Use regex or strip more carefully to get JSON
            content = response.text.strip()
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            data = json.loads(content)
            
            results = data.get('careers', [])
            if results and isinstance(results, list): 
                return results
                
        except Exception as e:
            print(f"Career Advice Error: {e}")
            
        # Fallback if AI fails or returns empty
        return [
            {"role": "Project Manager", "reason": "Requires strong organizational and interpersonal skills (Fallback Suggestion).", "industry": "Management"},
            {"role": "Data Analyst", "reason": "Suits analytical thinking and attention to detail (Fallback Suggestion).", "industry": "Tech"},
            {"role": "Human Resources", "reason": "Fits those with high empathy and people skills (Fallback Suggestion).", "industry": "HR"}
        ]

    @staticmethod
    def get_chat_response(topic_slug, user_message):
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Contextualize the chat
            system_instruction = f"You are an AI Tutor for {topic_slug} psychometric tests. Keep answers helpful, concise, and related to the topic."
            
            prompt = f"{system_instruction}\nUser: {user_message}\nTutor:"
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I'm having trouble connecting to my brain right now. (Error: {str(e)})"

    @staticmethod
    def generate_question(topic_slug):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment")

            model = genai.GenerativeModel('gemini-flash-latest')
            
            if topic_slug == 'verbal':
                prompt = AIContext.VERBAL_CONTEXT
            elif topic_slug == 'personality':
                prompt = AIContext.PERSONALITY_CONTEXT
            elif topic_slug == 'sjt':
                prompt = AIContext.SJT_CONTEXT
            else:
                return []

            response = model.generate_content(prompt)
            
            # Use regex or strip more carefully to get JSON
            content = response.text.strip()
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            data = json.loads(content)
            
            if "questions" in data:
                return data["questions"]
            return []
            
        except Exception as e:
            print(f"Gemini Generation Error: {e}")
            # Fallback to static questions if AI fails
            return AIService.get_fallback_questions(topic_slug)

    @staticmethod
    def get_fallback_questions(topic_slug):
        """Returns a list of 10 static questions based on the topic."""
        if topic_slug == 'verbal':
            return [
                {"type": "synonym", "text": "Synonym for 'Resilient'?", "options": ["Weak", "Strong", "Brittle", "Malleable"], "correct_index": 1, "explanation": "Resilient means able to withstand or recover quickly from difficult conditions.", "weight": 5},
                {"type": "sentence_completion", "text": "Despite the ____ of the situation, she remained calm.", "options": ["Severity", "Joy", "Peace", "Silence"], "correct_index": 0, "explanation": "Severity fits the context of remaining calm despite difficulty.", "weight": 5},
                {"type": "reading_comp", "text": "Passage: Solar energy is renewable. Statement: Solar panels only work in summer.", "options": ["True", "False", "Cannot Say"], "correct_index": 1, "explanation": "The passage doesn't support the statement; solar panels work in all seasons.", "weight": 5},
                {"type": "synonym", "text": "Synonym for 'Pragmatic'?", "options": ["Idealistic", "Practical", "Unrealistic", "Lazy"], "correct_index": 1, "explanation": "Pragmatic means dealing with things sensibly and realistically.", "weight": 5},
                {"type": "sentence_completion", "text": "The scientist's ____ approach led to a breakthrough.", "options": ["Haphazard", "Methodical", "Careless", "Random"], "correct_index": 1, "explanation": "Methodical research is most likely to lead to a breakthrough.", "weight": 5},
                {"type": "statement", "text": "Statement: All cats are mammals. Felix is a cat. Conclusion: Felix is a mammal.", "options": ["True", "False", "Cannot Say"], "correct_index": 0, "explanation": "Logical deduction follows the premise.", "weight": 5},
                {"type": "synonym", "text": "Synonym for 'Ambiguous'?", "options": ["Clear", "Vague", "Certain", "Bright"], "correct_index": 1, "explanation": "Ambiguous means open to more than one interpretation; not having one obvious meaning.", "weight": 5},
                {"type": "sentence_completion", "text": "The budget was ____ to meet the project's needs.", "options": ["Insufficient", "Abundant", "Enough", "Vast"], "correct_index": 0, "explanation": "Usually questions imply a constraint; insufficient fits if there's a problem.", "weight": 5},
                {"type": "reading_comp", "text": "Passage: The company's profits grew by 10%. Statement: The company is doing better than last year.", "options": ["True", "False", "Cannot Say"], "correct_index": 0, "explanation": "Growth in profits indicates better performance.", "weight": 5},
                {"type": "synonym", "text": "Synonym for 'Diligent'?", "options": ["Lazy", "Hardworking", "Fast", "Quiet"], "correct_index": 1, "explanation": "Diligent means having or showing care and conscientiousness in one's work.", "weight": 5}
            ]
        elif topic_slug == 'personality':
            return [
                {"type": "trait_based", "trait": "Extroversion", "text": "I enjoy meeting new people.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Agreeableness", "text": "I try to be kind to everyone.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Conscientiousness", "text": "I am always prepared.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Stability", "text": "I get stressed easily.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 5, "Disagree": 4, "Neutral": 3, "Agree": 2, "Strongly Agree": 1}},
                {"type": "trait_based", "trait": "Openness", "text": "I have a vivid imagination.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "forced_choice", "text": "Which describes you better?", "options": ["I prefer working alone", "I prefer working in a team"], "correct_index": -1, "weights": {"I prefer working alone": 1, "I prefer working in a team": 5}},
                {"type": "trait_based", "trait": "Order", "text": "I like to follow a schedule.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Empathy", "text": "I feel others' emotions.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Ambition", "text": "I set high goals for myself.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}},
                {"type": "trait_based", "trait": "Curiosity", "text": "I love learning how things work.", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], "correct_index": -1, "weights": {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}}
            ]
        elif topic_slug == 'sjt':
            return [
                {"competency": "Leadership", "text": "Your team is demotivated. What is your first step?", "options": ["Ignore them", "Host a meeting to listen", "Report to boss", "Give extra work"], "correct_index": 1, "explanation": "Listening to the team is the best first step.", "scores": [0, 5, 1, 0], "qualities": ["Very Poor", "Best", "Poor", "Very Poor"]},
                {"competency": "Prioritization", "text": "You have two deadlines today. One is from your boss, one from a peer.", "options": ["Do boss's first", "Do peer's first", "Do neither", "Ask for extension"], "correct_index": 0, "explanation": "Boss's deadlines usually take priority.", "scores": [5, 2, 0, 3], "qualities": ["Best", "Acceptable", "Very Poor", "Poor"]},
                {"competency": "Conflict", "text": "A colleague is rude in an email. How do you respond?", "options": ["Be rude back", "Ignore it", "Speak privately and calmly", "Reply all to complain"], "correct_index": 2, "explanation": "Private, calm communication resolves conflict best.", "scores": [0, 2, 5, 0], "qualities": ["Very Poor", "Acceptable", "Best", "Very Poor"]},
                {"competency": "Integrity", "text": "You notice an error in a report you already submitted.", "options": ["Hide it", "Wait for someone to find it", "Notify your manager immediately", "Blame someone else"], "correct_index": 2, "explanation": "Integrity means admitting errors and fixing them.", "scores": [0, 1, 5, 0], "qualities": ["Very Poor", "Poor", "Best", "Very Poor"]},
                {"competency": "Customer Service", "text": "A customer is shouting on the phone. What's your approach?", "options": ["Hang up", "Shout back", "Stay calm and listen", "Transfer them immediately"], "correct_index": 2, "explanation": "Staying calm and listening de-escalates situations.", "scores": [1, 0, 5, 2], "qualities": ["Poor", "Very Poor", "Best", "Acceptable"]},
                {"competency": "Adaptability", "text": "Your project scope changes halfway through. What do you do?", "options": ["Complain", "Quit", "Assess new requirements and plan", "Continue as before"], "correct_index": 2, "explanation": "Adaptability requires reassessing and planning.", "scores": [1, 0, 5, 0], "qualities": ["Poor", "Very Poor", "Best", "Very Poor"]},
                {"competency": "Efficiency", "text": "You found a way to automate a task, but your boss didn't ask for it.", "options": ["Don't do it", "Automate it and show results", "Wait for permission", "Keep it secret"], "correct_index": 1, "explanation": "Proactive efficiency is usually valued.", "scores": [2, 5, 3, 0], "qualities": ["Acceptable", "Best", "Poor", "Very Poor"]},
                {"competency": "Communication", "text": "You need to explain a complex topic to a non-technical client.", "options": ["Use jargon", "Use simple analogies", "Don't explain", "Give them a manual"], "correct_index": 1, "explanation": "Analogies help bridge the gap in understanding.", "scores": [0, 5, 0, 1], "qualities": ["Very Poor", "Best", "Very Poor", "Poor"]},
                {"competency": "Discipline", "text": "You feel distracted by social media at work. What do you do?", "options": ["Keep scrolling", "Set specific break times", "Delete your account", "Tell others to stop posting"], "correct_index": 1, "explanation": "Self-discipline involves setting boundaries.", "scores": [0, 5, 3, 0], "qualities": ["Very Poor", "Best", "Acceptable", "Very Poor"]},
                {"competency": "Teamwork", "text": "A teammate is struggling with their load. You are done with yours.", "options": ["Go home early", "Offer to help them", "Tell everyone you finished", "Ask for more work for yourself"], "correct_index": 1, "explanation": "Teamwork involves assisting colleagues.", "scores": [1, 5, 0, 2], "qualities": ["Poor", "Best", "Very Poor", "Acceptable"]}
            ]
        return []
