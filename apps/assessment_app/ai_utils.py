import os
import json
import difflib
import google.generativeai as genai
from django.conf import settings
from openai import AzureOpenAI

# Configuration
AI_PROVIDER = getattr(settings, 'AI_PROVIDER', 'gemini').lower()
GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', os.getenv("GOOGLE_API_KEY"))

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class CareerIntelligenceEngine:

    IDEAL_PROFILES = {
        "Data Scientist": {
            "logical": 9,
            "numerical": 9,
            "verbal": 6,
            "creative": 5,
            "empathy": 4
        },
        "Software Engineer": {
            "logical": 8,
            "numerical": 7,
            "verbal": 5,
            "creative": 4,
            "empathy": 4
        },
        "UX Designer": {
            "creative": 9,
            "verbal": 7,
            "empathy": 8,
            "logical": 5
        },
        "Product Manager": {
            "verbal": 8,
            "logical": 7,
            "empathy": 8,
            "creative": 6,
            "numerical": 5
        },
        "Numerical Reasoning": {  # Default for math-heavy paths
            "numerical": 9,
            "logical": 8,
            "verbal": 6,
            "creative": 5,
            "empathy": 4
        },
        "Logical Reasoning": {
            "logical": 9,
            "numerical": 8,
            "verbal": 6,
            "creative": 5,
            "empathy": 4
        },
        "Verbal Reasoning": {
            "verbal": 9,
            "logical": 7,
            "numerical": 5,
            "creative": 7,
            "empathy": 7
        },
        "Creative Thinking": {
            "creative": 9,
            "verbal": 8,
            "empathy": 8,
            "logical": 6,
            "numerical": 4
        },
        "Empathy/EQ": {
            "empathy": 9,
            "verbal": 8,
            "creative": 7,
            "logical": 6,
            "numerical": 5
        }
    }


    LEARNING_ACTIONS = {
        "logical": ["Practice DSA daily", "Solve competitive programming problems"],
        "numerical": ["Revise statistics", "Practice data interpretation sets"],
        "verbal": ["Improve writing skills", "Join public speaking workshops"],
        "creative": ["Build creative portfolio projects", "Participate in design challenges"],
        "empathy": ["Practice active listening", "Engage in team collaboration activities"]
    }

    @staticmethod
    def find_best_match(career_title):
        available = CareerIntelligenceEngine.IDEAL_PROFILES.keys()
        match = difflib.get_close_matches(
            career_title,
            available,
            n=1,
            cutoff=0.4
        )
        return match[0] if match else None

    @staticmethod
    def analyze(career_title, user_scores):
        matched = CareerIntelligenceEngine.find_best_match(career_title)

        if not matched:
            target_profile = {k: 7 for k in ["logical", "numerical", "verbal", "creative", "empathy"]}
        else:
            target_profile = CareerIntelligenceEngine.IDEAL_PROFILES[matched]

        # --- Skill Gap Analysis ---
        skill_gaps = []
        for skill, required in target_profile.items():
            current = user_scores.get(skill, 0)
            
            # --- EXCELLENCE LOGIC ---
            # If user already meets or exceeds the basic requirement, set an "Excellence Target"
            # This ensures even high-scorers get actionable "next steps".
            if current >= required:
                if current < 10:
                    target_val = 10
                    gap_type = "Excellence"
                else:
                    # Already at 10, no gap but maybe a mastery note
                    continue
            else:
                target_val = required
                gap_type = "Growth"

            gap_val = target_val - current

            if gap_val > 0:
                severity = (
                    "High" if gap_val >= 3 else
                    "Medium" if gap_val >= 2 else
                    "Low"
                )
                
                # Contextual recommendations
                if gap_type == "Excellence":
                    recommendations = [f"Master advanced {skill} concepts", f"Mentor others in {skill}"]
                    action_prefix = "Mastery: "
                else:
                    recommendations = CareerIntelligenceEngine.LEARNING_ACTIONS.get(skill, ["Upskill required"])
                    action_prefix = ""

                skill_gaps.append({
                    "skill": skill.title(),
                    "gap": gap_val,
                    "action": f"{action_prefix}{recommendations[0]}",
                    "severity": severity,
                    "type": gap_type
                })

        skill_gaps.sort(key=lambda x: (x["type"] == "Growth", x["gap"]), reverse=True)


        # --- Roadmap Generation ---
        roadmap_dict = {
            "Year 1": ["Master core fundamentals", "Earn 1–2 certifications", "Build 1 strong portfolio project"],
            "Year 2": ["Work on intermediate-level projects", "Start publishing on GitHub / LinkedIn", "Participate in hackathons"],
            "Year 3": [],
            "Year 4": [],
            "Year 5": []
        }

        # Correct Weak Skills Early
        for gap in skill_gaps:
            if gap["severity"] == "High":
                roadmap_dict["Year 1"].append(f"Focus heavily on improving {gap['skill']} skills")
            elif gap["severity"] == "Medium":
                roadmap_dict["Year 2"].append(f"Improve {gap['skill']} through structured learning")

        # Track-specific specialization
        if matched == "Data Scientist":
            roadmap_dict["Year 3"].extend(["Pursue internship in data analytics or ML", "Learn advanced Python, SQL, ML libraries"])
            roadmap_dict["Year 4"].append("Specialize in AI, ML, or Data Engineering")
            roadmap_dict["Year 5"].append("Lead data-driven projects or research initiatives")
        elif matched == "Software Engineer":
            roadmap_dict["Year 3"].append("Contribute to open-source projects")
            roadmap_dict["Year 4"].append("Specialize in backend, cloud, or AI systems")
            roadmap_dict["Year 5"].append("Move into senior engineer or architect role")
        elif matched == "UX Designer":
            roadmap_dict["Year 3"].append("Intern with UX/UI design teams")
            roadmap_dict["Year 4"].append("Specialize in UX research or motion design")
            roadmap_dict["Year 5"].append("Lead major product design initiatives")
        else:
            roadmap_dict["Year 3"].append("Focus on advanced certifications and specialized domains")
            roadmap_dict["Year 4"].append("Build leadership experience in chosen field")
            roadmap_dict["Year 5"].append("Establish yourself as a subject matter expert")

        # Accelerate Strong Skills
        for skill, score in user_scores.items():
            if isinstance(score, (int, float)) and score >= 8:
                roadmap_dict["Year 3"].append(f"Leverage strong {skill} skills for advanced competitions or leadership")

        # Format roadmap for template
        formatted_roadmap = []
        year_focus_map = {
            "Year 1": "Foundation & Baseline",
            "Year 2": "Intermediate Growth",
            "Year 3": "Specialization & Application",
            "Year 4": "Expertise Development",
            "Year 5": "Leadership & Mastery"
        }
        for i in range(1, 6):
            year_key = f"Year {i}"
            formatted_roadmap.append({
                "year": i,
                "focus": year_focus_map.get(year_key, "Career Growth"),
                "actions": roadmap_dict.get(year_key, ["Continue skill development"])
            })

        return {
            "career_match": matched or "General Professional",
            "skill_gap": skill_gaps,
            "roadmap": formatted_roadmap
        }

class AICareerService:
    # CATEGORY CONSTANTS for consistency
    CATEGORIES = {
        "logical": "Logical Reasoning",
        "numerical": "Numerical Reasoning",
        "verbal": "Verbal Reasoning",
        "creative": "Creative Thinking",
        "empathy": "Empathy/EQ"
    }

    @staticmethod
    def get_client():
        if AI_PROVIDER == 'azure':
            return AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
        return None

    @staticmethod
    def generate_questions(user_profile):
        all_questions = []
        
        for cat_key, cat_label in AICareerService.CATEGORIES.items():
            prompt = f"""
            You are an expert career counselor. Create 10 MCQ questions for a career assessment.
            Target Segment:
            - Age: {user_profile.get('age_group')}
            - Education: {user_profile.get('education')}
            - Experience: {user_profile.get('experience_level')}

            Category: {cat_label} (key: {cat_key})

            Requirements:
            - Generate exactly 10 Multiple Choice Questions (MCQs) for this specific category.
            - "category_key" MUST be "{cat_key}".
            - "category_label" MUST be "{cat_label}".
            - "correct_answer" must EXACTLY match the text of one of the options.
            - Provide 4 distinct options per question.

            Return strictly JSON in this format:
            {{
                "questions": [
                    {{
                        "id": 1,
                        "category_key": "{cat_key}",
                        "category_label": "{cat_label}",
                        "text": "Question text?",
                        "options": ["Opt A", "Opt B", "Opt C", "Opt D"],
                        "correct_answer": "Opt A"
                    }},
                    ... (total 10 questions for this category)
                ]
            }}
            
            CRITICAL: Only generate for the "{cat_label}" category. Every item in the "questions" list MUST be a full question object. Do NOT include placeholders.
            """

            try:
                if AI_PROVIDER == 'azure':
                    client = AICareerService.get_client()
                    response = client.chat.completions.create(
                        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"}
                    )
                    content = response.choices[0].message.content
                else:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    content = response.text.strip()
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()

                data = json.loads(content)
                cat_generated = data.get('questions', [])
                
                # HARDENING: Filter out non-dictionary items
                valid_cat_questions = [q for q in cat_generated if isinstance(q, dict)]
                all_questions.extend(valid_cat_questions)
                
            except Exception as e:
                print(f"Error generating questions for {cat_label}: {e}")
                # Fallback: add mock questions for ONLY this category if it fails
                all_questions.extend(AICareerService.get_mock_questions_for_category(cat_key, cat_label))

        # Re-index IDs to be sequential 1-50
        for i, q in enumerate(all_questions):
            q['id'] = i + 1
            
        return all_questions

    @staticmethod
    def get_mock_questions_for_category(key, label):
        questions = []
        for i in range(10):
            questions.append({
                "id": 0, # Will be re-indexed
                "category_key": key,
                "category_label": label,
                "text": f"Mock {label} Question {i+1}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A"
            })
        return questions

    @staticmethod
    def get_mock_questions():
        questions = []
        count = 1
        for key, label in AICareerService.CATEGORIES.items():
            for i in range(10):
                questions.append({
                    "id": count,
                    "category_key": key,
                    "category_label": label,
                    "text": f"Mock {label} Question {i+1}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                })
                count += 1
        return questions

    @staticmethod
    def calculate_scores(questions, user_answers):
        scores = {key: 0 for key in AICareerService.CATEGORIES.keys()}
        
        # Build lookup maps
        q_map = {str(q['id']): q for q in questions}

        for q_id, ans in user_answers.items():
            q = q_map.get(q_id)
            if not q: continue
            
            correct = str(q.get('correct_answer', '')).strip()
            user_ans = str(ans).strip()
            
            # Diagnostic Log
            print(f"DEBUG SCORING: QID={q_id}, Category={q.get('category_key')}, Correct='{correct}', User='{user_ans}'")
            
            # 1. Direct match
            match = (correct.lower() == user_ans.lower())
            
            # 2. Flexible match (Bidirectional substring match)
            if not match:
                clean_correct = correct.lower().split('.')[0].strip() # Handle "A." vs "A"
                clean_user = user_ans.lower().split('.')[0].strip()
                
                # Check labels match (e.g., correct="A", user="A. 10")
                if clean_correct in ['a', 'b', 'c', 'd', 'e'] and clean_user == clean_correct:
                    match = True
                
                # Check contents (e.g., correct="10", user="A. 10" OR correct="A. 10", user="10")
                if not match and len(correct) > 0 and len(user_ans) > 0:
                    if (correct.lower() in user_ans.lower()) or (user_ans.lower() in correct.lower()):
                        match = True

            if match:
                cat = str(q.get('category_key', '')).lower()
                # Flexibly match against internal keys or human-readable labels
                target_cat = None
                cat_aliases = {
                    "numerical": ["numerical reasoning", "math", "quantitative", "numbers"],
                    "logical": ["logical reasoning", "logic", "reasoning"],
                    "verbal": ["verbal reasoning", "english", "language"],
                    "creative": ["creative thinking", "creativity", "art"],
                    "empathy": ["empathy/eq", "empathy", "emotional intelligence", "eq"]
                }
                
                if cat in scores:
                    target_cat = cat
                else:
                    # Check aliases
                    for key, aliases in cat_aliases.items():
                        if cat in aliases or any(alias in cat for alias in aliases):
                            target_cat = key
                            break
                    
                    if not target_cat:
                        # Check labels
                        for key, label in AICareerService.CATEGORIES.items():
                            if cat == label.lower():
                                target_cat = key
                                break
                
                if target_cat:
                    scores[target_cat] += 1
        
        # Derived fields
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        scores['primary_track'] = sorted_scores[0][0] if sorted_scores else "N/A"
        scores['secondary_track'] = sorted_scores[1][0] if len(sorted_scores) > 1 else "N/A"
        scores['total'] = sum(v for k, v in scores.items() if k in AICareerService.CATEGORIES)
        
        return scores

    @staticmethod
    def generate_career_insights(scores, user_profile):
        """
        Generates deep insights using a hybrid approach:
        1. Rule-based CareerIntelligenceEngine for skill gaps and roadmaps.
        2. AI for creative career descriptions and match justification.
        """
        # 1. Deterministic Analysis via Engine
        # We use the primary track as the starting point for career matching
        primary_track_label = AICareerService.CATEGORIES.get(scores.get('primary_track'), "General")
        engine_results = CareerIntelligenceEngine.analyze(primary_track_label, scores)

        # 2. AI Enhancement for Career Recommendations
        prompt = f"""
        Analyze these career assessment scores: {json.dumps(scores)}
        User Profile: {json.dumps(user_profile)}
        Best Rule-Based Match: {engine_results['career_match']}

        Generate a detailed JSON report for 3 recommended careers.
        Return strictly JSON:
        {{
            "careers": [
                {{"role": "Role Name", "description": "Justify why this fits based on their specific scores", "match_score": "95%"}},
                ...
            ]
        }}
        """

        try:
            if AI_PROVIDER == 'azure':
                client = AICareerService.get_client()
                response = client.chat.completions.create(
                    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                content = response.choices[0].message.content
            else:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                content = response.text.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()

            ai_careers = json.loads(content).get('careers', [])
        except Exception as e:
            print(f"Error enhancing with AI: {e}")
            ai_careers = [{"role": engine_results['career_match'], "description": "Highly recommended based on your aptitude profile.", "match_score": "90%"}]

        # 3. Combine Results
        return {
            "skill_gap": engine_results['skill_gap'],
            "roadmap": engine_results['roadmap'],
            "careers": ai_careers,
            "career_match": engine_results['career_match']
        }
