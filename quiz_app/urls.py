from django.urls import path
from . import views

# URL patterns for the quiz_app
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]