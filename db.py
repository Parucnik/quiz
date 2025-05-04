import sqlite3


with sqlite3.connect('quizzes.db') as conn:
    cur = conn.cursor()
    cur.execute(
    '''DROP TABLE IF EXISTS question''')
    cur.execute(
    '''DROP TABLE IF EXISTS quiz''')
    cur.execute(
    '''DROP TABLE IF EXISTS quiz_content''')
    cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS quiz
    (id INTEGER PRIMARY KEY,
    name VARCHAR)
    ''')
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS question
    (id INTEGER PRIMARY KEY,
    question VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS quiz_content
                (id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id)
                )
                ''')
    cur.execute('''PRAGMA foreign_keys=on''')
    conn.commit()
with sqlite3.connect('quizzes.db') as conn:
    cur = conn.cursor()
    list_q = [('Сколько месяцев в году имеют 28 дней?', 
           'Все', 'Один', 'Ни одного', 'Два'),
          ('Чему равно число Пи?', 
           'Примерно 3.14', '3', '0', 'Ровно 3.14'), 
           ('Формула воды?', 'H20', 'HCl', 'H2', 'O3')]

    cur.executemany('''INSERT INTO question 
                 (question, answer, wrong1, wrong2, wrong3) 
                  VALUES (?,?,?,?,?)''', list_q)
    
    cur.executemany('''INSERT INTO quiz (name) 
                     VALUES (?)''', [('Мощь мозгов',), ('Немощь мозга',)])
    
    cur.executemany('''INSERT INTO quiz_content (quiz_id, question_id) 
                VALUES (?, ?)''', [(1,1), (1,2), (2,2), (2,3), (2,1)])
    conn.commit()

def get_question(q_id):
    with sqlite3.connect('quizzes.db') as conn:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM question WHERE id = {q_id}''')
        return cur.fetchall()[0]

def get_all_quiz():
    ''' Функция возвращает список все викторин'''
    with sqlite3.connect('quizzes.db') as conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM quiz''')
        return cur.fetchall()

def get_questions_by_quiz(quiz_id):
    with sqlite3.connect('quizzes.db') as conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM question 
                    JOIN quiz_content ON question.id = quiz_content.question_id
                    WHERE quiz_content.quiz_id = ?''', (quiz_id,))
        return cur.fetchall()