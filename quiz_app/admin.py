from django.contrib import admin
from .models import Quiz, Question, Choice, Score

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Score)
