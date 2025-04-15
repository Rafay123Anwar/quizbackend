import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

# Configure API key for Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def generate_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic', '')  # Get the topic from request data

            if not topic:
                return JsonResponse({"error": "Topic is required"}, status=400)

            # Define prompt for the Gemini API to generate a quiz
            prompt = f"""
            You are an API that generates quizzes. Return only JSON.
            Create a 10-question multiple choice quiz on the topic '{topic}'.
            Each question should have:
            - "question" (string)
            - "options" (dictionary with keys A, B, C, D)
            - "answer" (correct option as one of A, B, C, or D)

            Example Format:
            {{
                "topic": "{topic}",
                "questions": [
                    {{
                        "question": "Sample Question?",
                        "options": {{
                            "A": "Option A",
                            "B": "Option B",
                            "C": "Option C",
                            "D": "Option D"
                        }},
                        "answer": "B"
                    }}
                ]
            }}
            """

            # Generate quiz using Gemini API
            model = genai.GenerativeModel("models/gemini-1.5-pro")
            response = model.generate_content(prompt)

            # Process the response and return the quiz in JSON format
            content = response.text.strip().replace('```json', '').replace('```', '')
            
            try:
                quiz_json = json.loads(content)  # Parse the content as JSON
                return JsonResponse(quiz_json)  # Return the generated quiz
            except json.JSONDecodeError:
                return JsonResponse({"raw_text": content, "error": "Could not parse response as JSON"}, status=500)

        except Exception as e:
            print("Error occurred:", str(e))  # Log error on the server
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

@csrf_exempt
def submit_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user_answers = data.get("answers")
            quiz = data.get("quiz")

            if not quiz:
                return JsonResponse({"error": "No quiz found"}, status=400)

            score = 0
            correct_answers = {}

            for idx, q in enumerate(quiz['questions']):
                correct = q["answer"]
                correct_answers[str(idx)] = correct

                if user_answers.get(str(idx)) == correct:
                    score += 1

            return JsonResponse({
                "score": score,
                "total": len(quiz['questions']),
                "correct_answers": correct_answers  # ✅ Return this
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


