from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import bcrypt
import random

app = Flask(__name__)
app.secret_key = 'signmaster_secret_key'

# ---------------- DB CONNECTION ----------------
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        database="signmaster",
        user="postgres",
        password="system"
    )

# ---------------- FETCH QUIZ QUESTIONS ----------------
def get_quiz_questions(quiz_id):
    """
    Fetch all questions for the quiz, shuffle questions and options.
    Returns a list of dicts:
    {'question_text', 'question_image', 'answer', 'options'}
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT question_text, question_image, answer, options FROM questions WHERE quiz_id=%s ORDER BY id",
        (quiz_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    questions = []
    for row in rows:
        # row[3] is already a list in PostgreSQL (ARRAY), no need to split
        opts = list(row[3]) if row[3] else []
        # Ensure the correct answer is included
        if row[2] not in opts:
            opts.append(row[2])
        random.shuffle(opts)  # shuffle options
        questions.append({
            'question_text': row[0],
            'question_image': row[1],
            'answer': row[2],
            'options': opts
        })

    random.shuffle(questions)  # shuffle questions order
    return questions

# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('quiz_list'))
    return redirect(url_for('login'))

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            flash("No account found. Please sign up first.", "error")
            return redirect(url_for('signup'))

        stored_hash = user[0]
        if not bcrypt.checkpw(password, stored_hash.encode('utf-8')):
            flash("Incorrect password.", "error")
            return redirect(url_for('login'))

        session['username'] = username
        return redirect(url_for('quiz_list'))

    return render_template('login.html')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].encode('utf-8')

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed.decode('utf-8'))
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except Exception:
            flash("Username or Email already exists!", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# ---------------- QUIZ LIST ----------------
@app.route('/quiz')
def quiz_list():
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM quizzes ORDER BY id")
    quizzes = cur.fetchall()
    cur.close()
    conn.close()

    if not quizzes:
        flash("No quizzes available.", "error")
    return render_template('quiz_list.html', quizzes=quizzes, username=session['username'])

# ---------------- LEARNING ----------------
@app.route('/learn/<int:quiz_id>')
def learn(quiz_id):
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    idx = request.args.get('idx', default=0, type=int)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, question_text, question_image, answer FROM questions WHERE quiz_id=%s ORDER BY id",
        (quiz_id,)
    )
    items = cur.fetchall()
    cur.close()
    conn.close()

    if not items:
        flash("This quiz has no learning items.", "error")
        return redirect(url_for('quiz_list'))

    total = len(items)
    if idx < 0: idx = 0
    if idx >= total: idx = total - 1

    item = {
        'id': items[idx][0],
        'question_text': items[idx][1],
        'question_image': items[idx][2],
        'answer': items[idx][3]
    }

    return render_template('learn.html',
                           quiz_id=quiz_id,
                           item=item,
                           idx=idx,
                           total=total)

# ---------------- MULTI-QUESTION QUIZ ----------------
@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    # Fetch questions for this quiz
    questions = get_quiz_questions(quiz_id)  # returns a list of dicts
    total = len(questions)

    # Initialize session for quiz progress
    if 'quiz_progress' not in session or session.get('quiz_progress', {}).get('quiz_id') != quiz_id:
        session['quiz_progress'] = {'quiz_id': quiz_id, 'current': 0, 'score': 0, 'answers': []}

    progress = session['quiz_progress']
    idx = progress['current']
    question = questions[idx]

    if request.method == 'POST':
        selected_option = request.form['option']
        progress['answers'].append(selected_option)
        if selected_option == question['answer']:
            progress['score'] += 1

        progress['current'] += 1
        session['quiz_progress'] = progress

        # If finished, show result
        if progress['current'] >= total:
            score = progress['score']
            session.pop('quiz_progress')  # reset
            return render_template('quiz_result.html', score=score, total=total)

        return redirect(url_for('take_quiz', quiz_id=quiz_id))  # next question

    return render_template('quiz_multi.html', quiz=question, current=idx+1, total=total)

# ---------------- STATIC PAGES ----------------
@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help_page():
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))
    return render_template('help.html')

# ---------------- PROFILE ----------------
@app.route('/profile')
def profile():
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    username = session['username']

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Fetch only username and email
        cur.execute("SELECT username, email FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB Error:", e)
        flash("Unable to fetch user data.", "error")
        return redirect(url_for('quiz_list'))

    if not user:
        flash("User not found.", "error")
        return redirect(url_for('quiz_list'))

    user_dict = {
        'username': user[0],
        'email': user[1]
    }

    return render_template('profile.html', user=user_dict)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
