from apps.assessment_app.models import CareerAssessment
import json

a = CareerAssessment.objects.latest('id')
print(f"Assessment ID: {a.id}")
print(f"Scores: {a.scores}")

questions = a.questions_data
answers = a.answers_data

print(f"\nTotal Questions: {len(questions)}")
print(f"Total Answers: {len(answers)}")

sample_count = 0
for q in questions:
    q_id = str(q['id'])
    correct = q.get('correct_answer')
    ans = answers.get(q_id)
    
    if sample_count < 5:
        print(f"\nQ_ID: {q_id}")
        print(f"Correct: {repr(correct)} ({type(correct)})")
        print(f"User Ans: {repr(ans)} ({type(ans)})")
        print(f"Match: {str(correct) == str(ans)}")
    
    sample_count += 1
