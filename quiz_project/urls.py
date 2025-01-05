from django.contrib import admin
from django.urls import path, include

# URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('', include('quiz_app.urls')),  # Include URLs from the quiz_app
]
