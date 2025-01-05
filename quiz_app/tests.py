from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quiz, Question, Choice, Score, UserAnswer

class QuizAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.quiz = Quiz.objects.create(title='Sample Quiz', description='Sample Description')
        self.question1 = Question.objects.create(quiz=self.quiz, text='Question 1')
        self.question2 = Question.objects.create(quiz=self.quiz, text='Question 2')
        self.choice1 = Choice.objects.create(question=self.question1, text='Choice 1', is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question1, text='Choice 2', is_correct=False)
        self.choice3 = Choice.objects.create(question=self.question2, text='Choice 3', is_correct=True)
        self.choice4 = Choice.objects.create(question=self.question2, text='Choice 4', is_correct=False)

    def test_quiz_creation(self):
        self.assertEqual(self.quiz.title, 'Sample Quiz')
        self.assertEqual(self.quiz.description, 'Sample Description')

    def test_question_creation(self):
        self.assertEqual(self.question1.text, 'Question 1')
        self.assertEqual(self.question2.text, 'Question 2')

    def test_choice_creation(self):
        self.assertEqual(self.choice1.text, 'Choice 1')
        self.assertTrue(self.choice1.is_correct)
        self.assertEqual(self.choice2.text, 'Choice 2')
        self.assertFalse(self.choice2.is_correct)

    def test_user_answer(self):
        user_answer1 = UserAnswer.objects.create(user=self.user, question=self.question1, choice=self.choice1)
        user_answer2 = UserAnswer.objects.create(user=self.user, question=self.question2, choice=self.choice4)
        self.assertEqual(user_answer1.choice, self.choice1)
        self.assertEqual(user_answer2.choice, self.choice4)

    def test_score_calculation(self):
        UserAnswer.objects.create(user=self.user, question=self.question1, choice=self.choice1)
        UserAnswer.objects.create(user=self.user, question=self.question2, choice=self.choice4)
        score, total, results = Score.calculate_score(user=self.user, quiz=self.quiz)
        self.assertEqual(score, 1)
        self.assertEqual(total, 2)
        self.assertEqual(results[self.question1.text]['user_answer'], 'Choice 1')
        self.assertEqual(results[self.question1.text]['correct_answer'], 'Choice 1')
        self.assertEqual(results[self.question2.text]['user_answer'], 'Choice 4')
        self.assertEqual(results[self.question2.text]['correct_answer'], 'Choice 3')
