# # # # from rest_framework.views import APIView
# # # # from rest_framework.response import Response
# # # # from rest_framework import status
# # # # import openai
# # # # import os
# # # # import json
# # # # from openai import OpenAI

# # # # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # # # class GenerateQuizView(APIView):
# # # #     def post(self, request):
# # # #         topic = request.data.get("topic")
# # # #         if not topic:
# # # #             return Response({"error": "Topic is required"}, status=400)

# # # #         prompt = f"""
# # # #         Generate 10 multiple-choice questions (MCQs) on the topic '{topic}' in JSON format like this:
# # # #         [
# # # #             {{
# # # #                 "question": "Question text?",
# # # #                 "options": ["Option A", "Option B", "Option C", "Option D"],
# # # #                 "answer": "Correct Option"
# # # #             }},
# # # #             ...
# # # #         ]
# # # #         """

# # # #         try:
# # # #             response = client.chat.completions.create(
# # # #                 model="gpt-3.5-turbo",
# # # #                 messages=[{"role": "user", "content": prompt}],
# # # #                 temperature=0.7
# # # #             )
# # # #             content = response.choices[0].message.content
# # # #             quiz = json.loads(content)
# # # #             request.session['quiz'] = quiz
# # # #             return Response(quiz)
# # # #         except Exception as e:
# # # #             return Response({"error": str(e)}, status=500)


# # # # class SubmitQuizView(APIView):
# # # #     def post(self, request):
# # # #         user_answers = request.data.get("answers")
# # # #         quiz = request.session.get('quiz')
# # # #         if not quiz:
# # # #             return Response({"error": "No quiz found in session"}, status=400)

# # # #         score = 0
# # # #         for idx, q in enumerate(quiz):
# # # #             if q["answer"] == user_answers.get(str(idx)):
# # # #                 score += 1

# # # #         return Response({
# # # #             "score": score,
# # # #             "total": len(quiz)
# # # #         })


# # # # import openai
# # # # from django.http import JsonResponse
# # # # from django.views.decorators.csrf import csrf_exempt
# # # # import json
# # # # from django.conf import settings

# # # # openai.api_key = settings.OPENAI_API_KEY

# # # # @csrf_exempt
# # # # def generate_quiz(request):
# # # #     if request.method == 'POST':
# # # #         try:
# # # #             data = json.loads(request.body)
# # # #             topic = data.get('topic', '')

# # # #             prompt = (
# # # #                 f"Create a 10-question multiple choice quiz on the topic '{topic}'. "
# # # #                 f"Each question should have 4 options (A, B, C, D) and indicate the correct answer."
# # # #             )

# # # #             response = openai.chat.completions.create(
# # # #                 model="gpt-3.5-turbo",
# # # #                 messages=[
# # # #                     {"role": "user", "content": prompt}
# # # #                 ],
# # # #                 temperature=0.7,
# # # #                 max_tokens=1000
# # # #             )

# # # #             content = response.choices[0].message.content
# # # #             return JsonResponse({"quiz": content})
        
# # # #         except Exception as e:
# # # #             return JsonResponse({"error": str(e)}, status=500)
# # # #     return JsonResponse({"error": "Only POST method allowed"}, status=405)


# # # import google.generativeai as genai
# # # from django.http import JsonResponse
# # # from django.views.decorators.csrf import csrf_exempt
# # # import json
# # # from django.conf import settings

# # # genai.configure(api_key=settings.GEMINI_API_KEY)

# # # @csrf_exempt
# # # def generate_quiz(request):
# # #     if request.method == 'POST':
# # #         try:
# # #             data = json.loads(request.body)
# # #             topic = data.get('topic', '')

# # #             prompt = f"""
# # # You are an API that generates quizzes. Return only JSON.
# # # Create a 10-question multiple choice quiz on the topic '{topic}'.
# # # Each question should have:
# # # - "question" (string)
# # # - "options" (dictionary with keys A, B, C, D)
# # # - "answer" (correct option as one of A, B, C, or D)

# # # Example Format:
# # # {{
# # #   "topic": "{topic}",
# # #   "questions": [
# # #     {{
# # #       "question": "Sample?",
# # #       "options": {{
# # #         "A": "Option A",
# # #         "B": "Option B",
# # #         "C": "Option C",
# # #         "D": "Option D"
# # #       }},
# # #       "answer": "B"
# # #     }}
# # #   ]
# # # }}
# # # """

# # #             model = genai.GenerativeModel("models/gemini-1.5-pro")
# # #             response = model.generate_content(prompt)
# # #             # Strip the response text and remove markdown
# # #             content = response.text.strip().replace('```json', '').replace('```', '')

# # #             try:
# # #                 # Now attempt to parse it as JSON
# # #                 quiz_json = json.loads(content)
# # #                 return JsonResponse(quiz_json)
# # #             except json.JSONDecodeError:
# # #                 return JsonResponse({"raw_text": content, "error": "Could not parse response as JSON"}, status=500)

# # #         except Exception as e:
# # #             return JsonResponse({"error": str(e)}, status=500)

# # #     return JsonResponse({"error": "Only POST method allowed"}, status=405)


# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # import json
# # import os
# # import requests

# # # Replace with your Gemini API key or relevant API setup
# # GEMINI_API_KEY = os.getenv("AIzaSyA9uutkgaL7o_IGLdBNFIsg2hnqEL0MBck")
# # GEMINI_API_URL = "https://api.gemini.com/v1/generate_quiz" 

# # @csrf_exempt
# # def generate_quiz(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             topic = data.get('topic', '')

# #             if not topic:
# #                 return JsonResponse({"error": "Topic is required"}, status=400)

# #             prompt = f"Create a 10-question multiple-choice quiz on the topic '{topic}'. Each question should have 4 options (A, B, C, D) and indicate the correct answer."

# #             # Send request to Gemini API for quiz generation
# #             response = requests.post(
# #                 GEMINI_API_URL,
# #                 headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
# #                 json={"prompt": prompt}
# #             )

# #             if response.status_code == 200:
# #                 quiz_data = response.json()
# #                 return JsonResponse({"quiz": quiz_data})
# #             else:
# #                 return JsonResponse({"error": "Failed to generate quiz"}, status=500)
        
# #         except Exception as e:
# #             return JsonResponse({"error": str(e)}, status=500)
    
# #     return JsonResponse({"error": "Only POST method allowed"}, status=405)


# # # from django.http import JsonResponse
# # # from django.views.decorators.csrf import csrf_exempt
# # # import json

# # @csrf_exempt
# # def submit_quiz(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             user_answers = data.get("answers")
# #             quiz = data.get("quiz")

# #             if not quiz:
# #                 return JsonResponse({"error": "No quiz found"}, status=400)

# #             score = 0
# #             for idx, q in enumerate(quiz['questions']):
# #                 if q["answer"] == user_answers.get(str(idx)):
# #                     score += 1

# #             return JsonResponse({
# #                 "score": score,
# #                 "total": len(quiz['questions'])
# #             })

# #         except Exception as e:
# #             return JsonResponse({"error": str(e)}, status=500)

# #     return JsonResponse({"error": "Only POST method allowed"}, status=405)

# import google.generativeai as genai
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.conf import settings

# # Configure Gemini API with the API key from Django settings
# genai.configure(api_key=settings.GEMINI_API_KEY)

# @csrf_exempt
# def generate_quiz(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             topic = data.get('topic', '')

#             if not topic:
#                 return JsonResponse({"error": "Topic is required"}, status=400)

#             prompt = f"""
#             You are an API that generates quizzes. Return only JSON.
#             Create a 10-question multiple choice quiz on the topic '{topic}'.
#             Each question should have:
#             - "question" (string)
#             - "options" (dictionary with keys A, B, C, D)
#             - "answer" (correct option as one of A, B, C, or D)

#             Example Format:
#             {{
#               "topic": "{topic}",
#               "questions": [
#                 {{
#                   "question": "Sample?",
#                   "options": {{
#                     "A": "Option A",
#                     "B": "Option B",
#                     "C": "Option C",
#                     "D": "Option D"
#                   }},
#                   "answer": "B"
#                 }}
#               ]
#             }}
#             """

#             # Using Google Gemini API to generate quiz content
#             model = genai.GenerativeModel("models/gemini-1.5-pro")
#             response = model.generate_content(prompt)

#             # Strip the response text and remove markdown formatting
#             content = response.text.strip().replace('```json', '').replace('```', '')

#             try:
#                 # Attempt to parse the response content as JSON
#                 quiz_json = json.loads(content)
#                 return JsonResponse(quiz_json)
#             except json.JSONDecodeError:
#                 # If unable to parse, return the raw response text with an error
#                 return JsonResponse({"raw_text": content, "error": "Could not parse response as JSON"}, status=500)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Only POST method allowed"}, status=405)


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def submit_quiz(request):
#     if request.method == 'POST':
#         try:
#             # Parse the incoming JSON data
#             data = json.loads(request.body)
#             user_answers = data.get("answers")  # User's submitted answers
#             quiz = data.get("quiz")  # The quiz object to compare answers against

#             # Validate that quiz is present
#             if not quiz:
#                 return JsonResponse({"error": "No quiz found"}, status=400)

#             # Ensure answers are provided
#             if not user_answers:
#                 return JsonResponse({"error": "User answers are required"}, status=400)

#             score = 0
#             total_questions = len(quiz['questions'])

#             # Check each question's answer
#             for idx, question in enumerate(quiz['questions']):
#                 correct_answer = question["answer"]
#                 user_answer = user_answers.get(str(idx))  # Compare by index

#                 # If the user's answer matches the correct answer, increase the score
#                 if user_answer == correct_answer:
#                     score += 1

#             # Return the score and total questions
#             return JsonResponse({
#                 "score": score,
#                 "total": total_questions
#             })

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     # Return error for non-POST requests
#     return JsonResponse({"error": "Only POST method allowed"}, status=405)


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
