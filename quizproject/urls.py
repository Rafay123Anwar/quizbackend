from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"message": "Quiz backend is running!"})


urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/', include('quiz.urls')),  # Ensure there's a slash after 'api'
]
