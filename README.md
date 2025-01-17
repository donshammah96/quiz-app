# Quiz App

This is a Django-based quiz application that allows users to register, take timed quizzes, and track their scores.

## Features

- User registration and authentication
- Timed quizzes
- Score tracking
- Responsive design using Bootstrap

## Requirements

- Python 3.x
- Django 3.2.x

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/donshammah96/quiz-app.git
    cd quiz-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/` to see the application.

## Usage

- Register a new user or log in with an existing account.
- Browse the list of available quizzes.
- Take a quiz and submit your answers.
- View your scores and track your progress.

## Project Structure

```
quiz-app/
├── quiz_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── quiz_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   ├── register.html
│   │   ├── quiz_list.html
│   │   ├── quiz_detail.html
│   └── migrations/
│       └── __init__.py
├── manage.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
