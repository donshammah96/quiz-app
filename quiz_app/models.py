from django.contrib.auth.models import User
from django.db import models

# Model for Quiz
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    @classmethod
    def create_quiz(cls, title, description):
        quiz = cls(title=title, description=description)
        quiz.save()
        return quiz

# Model for Question
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    @classmethod
    def create_question(cls, quiz, text):
        question = cls(quiz=quiz, text=text)
        question.save()
        return question

# Model for Choice
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    @classmethod
    def create_choice(cls, question, text, is_correct=False):
        choice = cls(question=question, text=text, is_correct=is_correct)
        choice.save()
        return choice

    @classmethod
    def get_choices_for_question(cls, question):
        return cls.objects.filter(question=question)

# Model for Score
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)
    results = models.JSONField(default=dict)  # Add this line to store results as JSON

    @classmethod
    def create_score(cls, user, quiz, score, total, results):
        score_entry = cls(user=user, quiz=quiz, score=score, total=total, results=results)
        score_entry.save()
        return score_entry


    @classmethod
    def calculate_score(cls, user, quiz):
        questions = Question.objects.filter(quiz=quiz)
        total = questions.count()
        correct_answers = 0
        results = {}
        for question in questions:
            try:
                user_answer = UserAnswer.objects.get(user=user, question=question)
                correct_answer = Choice.objects.get(question=question, is_correct=True)
                results[question.text] = {
                    'user_answer': user_answer.choice.text,
                    'correct_answer': correct_answer.text
                }
                if user_answer.choice == correct_answer:
                    correct_answers += 1
            except UserAnswer.DoesNotExist:
                correct_answer = Choice.objects.filter(question=question, is_correct=True).first()
                results[question.text] = {
                    'user_answer': 'No answer given',
                    'correct_answer': correct_answer.text if correct_answer else 'No correct answer'
                }
            except Choice.DoesNotExist:
                results[question.text] = {
                    'user_answer': user_answer.choice.text if user_answer else 'No answer given',
                    'correct_answer': 'No correct answer'
                }
        score = correct_answers
        return score, total, results

# Model for UserAnswer
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.choice.text}"