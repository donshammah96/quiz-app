import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Quiz, Question, Score, Choice

logger = logging.getLogger(__name__)

# View for user registration
def register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('quiz_list')
        else:
            form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in register view: {e}")
        return render(request, 'error.html')

# View for user login
def user_login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('quiz_list')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in user_login view: {e}")
        return render(request, 'error.html')

# View for user logout
def user_logout(request):
    try:
        logout(request)
        return redirect('quiz_list')
    except Exception as e:
        logger.error(f"Error in user_logout view: {e}")
        return render(request, 'error.html')

# View for landing page
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('quiz_list')
    else:
        return render(request, 'landing_page.html')

# View to list all quizzes
def quiz_list(request):
    try:
        quizzes = Quiz.objects.all()
        return render(request, 'quiz_list.html', {'quizzes': quizzes})
    except Exception as e:
        logger.error(f"Error in quiz_list view: {e}")
        return render(request, 'error.html')

# View to display quiz details and questions
def quiz_detail(request, quiz_id):
    try:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})
    except Exception as e:
        logger.error(f"Error in quiz_detail view: {e}")
        return render(request, 'error.html')

def submit_quiz(request, quiz_id):
    try:
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        score = 0
        total = questions.count()  # Total number of questions in the quiz
        results = []  # List to store the user's answers and their correctness

        for question in questions:
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                choice = Choice.objects.get(pk=selected_choice_id)
                is_correct = choice.is_correct
                results.append({
                    'question': question.text,
                    'selected_choice': choice.text,
                    'is_correct': is_correct
                })
                if is_correct:
                    score += 1
            else:
                results.append({
                    'question': question.text,
                    'selected_choice': None,
                    'is_correct': False
                })

        # Save the score to the database
        Score.objects.create(user=request.user, quiz=quiz, score=score)

        # Pass all necessary context to the template
        context = {
            'quiz': quiz,
            'score': score,
            'total': total,
            'results': results
        }
        return render(request, 'quiz_result.html', context)
    except Exception as e:
        logger.error(f"Error in submit_quiz view: {e}")
        return render(request, 'error.html')


def quiz_result_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user

    # Calculate the score, total, and results using the Score model method
    score, total, results = Score.calculate_score(user=user, quiz=quiz)

    # Save the score in the database
    Score.create_score(user=user, quiz=quiz, score=score, total=total, results=results)

    # Pass all required context to the template
    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'score': score,
        'total': total,
        'results': results,
    })
