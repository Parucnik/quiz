# Здесь будет код веб-приложения
from flask import Flask, redirect, render_template, request, session
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def index():
    if request.method == 'POST':
        session['quiz_id'] = request.form.get('quiz_id')
        return redirect('test')
    quizes: list[tuple] = db.get_all_quiz()
    session['count'] = 0
    session['amount_correct'] = 0
    return render_template('start.html', quizes=quizes)

def test():
    if not session.get('amount_correct'):
        session['amount_correct'] = 0

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == session['correct_answer']:
            session['amount_correct'] += 1
        session['count'] += 1
    # 1. Получить все вопросы выбранной викторины
    questions: list[tuple] = db.get_questions_by_quiz(session['quiz_id'])
    # 2. Выберем один вопрос
    if not session.get('count'):
        session['count'] = 0
    try:
        selected_question: tuple = questions[session['count']]
    except IndexError:
        return redirect('result')
    # 3. Отобразить вопрос и ответы в шаблоне
    text: str = selected_question[1]
    answers: tuple = selected_question[2:6]
    session['correct_answer'] = selected_question[2]

    
    return render_template('test.html', info=str(questions), \
                           text_question=text, answers=answers)

def result():
    # 1. Количество заданных вопросов
    amount_questions = len(db.get_questions_by_quiz(session['quiz_id']))
    # 2. Количество правильных ответов
    correct_answers = session['amount_correct']
    # 3. Процент правильных ответов
    percent_correct = int((correct_answers / amount_questions) * 100)
    return render_template('result.html', amount_questions=amount_questions,\
                            correct_answers=correct_answers, percent_correct=percent_correct)

app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods=['GET', 'POST'])
app.add_url_rule('/result', 'result', result)
app.run(debug=True)

