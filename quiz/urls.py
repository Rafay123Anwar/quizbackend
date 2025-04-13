# from django.urls import path
# from .views import generate_quiz, submit_quiz

# urlpatterns = [
#     path('generate/', generate_quiz.as_view()),
#     path('submit/', submit_quiz.as_view()),
    
# ]

# # from django.urls import path
# # from .views import generate_quiz

# # urlpatterns = [
# #     path('generate/', generate_quiz, name='generate_quiz'),
# # ]

from django.urls import path
from . import views

urlpatterns = [
    path('generate-quiz/', views.generate_quiz, name='generate_quiz'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
]
