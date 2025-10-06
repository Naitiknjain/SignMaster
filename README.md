# SignMaster – Interactive Sign Language Learning & Quiz Platform

## 📌 About the Project
SignMaster is a **web-based application** developed using **Flask and PostgreSQL** to help users **learn sign language** and test their knowledge through interactive quizzes.  
Users can **sign up, log in, view learning materials**, take quizzes with **randomized questions**, and track their performance at the end of the quiz.

---

## 🎯 Features
- **User Authentication**: Sign up, login, and logout securely with hashed passwords using bcrypt.  
- **Learning Modules**: Access learning content with text and images for each sign language lesson.  
- **Interactive Quizzes**:  
  - Multi-question quizzes with **randomized questions**  
  - Options displayed as buttons  
  - **Score calculated** at the end, no hints about previous questions  
- **Profile Page**: View your username and email.  
- **Static Pages**: About, Reviews, and Help pages.  
- **Responsive & Styled Interface**: Clean navigation and intuitive UI.

---

## 🛠 Tools & Technologies
- **Backend**: Python, Flask, psycopg2  
- **Frontend**: HTML, CSS, Jinja2 Templates  
- **Database**: PostgreSQL  
- **Authentication**: bcrypt for password hashing  
- **Randomization**: Python’s `random` module to shuffle quiz questions

---

## 📂 Folder Structure
```text
SignMaster/
│
├── app.py                  # Main Flask application
├── db_config.py            # Database connection configuration
├── templates/              # HTML templates
│   ├── login.html
│   ├── signup.html
│   ├── quiz_list.html
│   ├── quiz_multi.html
│   ├── quiz_result.html
│   ├── learn.html
│   ├── profile.html
│   ├── reviews.html
│   ├── help.html
│   └── about.html
├── static/                 # CSS, JS, images
│   └── images/
│       ├── quiz1/          # Quiz 1 images (A.png, B.png, …)
│       ├── quiz2/          # Quiz 2 images
│       ├── quiz3/          # Quiz 3 images
│       └── quiz4/          # Quiz 4 images
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

---

## 🚀Installation & Setup

-Clone the repository:

    git clone https://github.com/Naitiknjain/SignMaster.git
    cd jhingalala


-Create a virtual environment (optional but recommended):

    python -m venv venv
    # On Linux/macOS
    source venv/bin/activate
    # On Windows
    venv\Scripts\activate


-Install dependencies:

    pip install -r requirements.txt


-Configure PostgreSQL Database:

    Create a database named signmaster.
    Update credentials in db_config.py if needed.
    Ensure the users, quizzes, and questions tables are created with correct columns.
    Run the Flask app:
    python app.py

-Open your browser at:

    http://127.0.0.1:5000

---

##🎮 How to Use

    Sign up for a new account or login with existing credentials.
    Browse available quizzes and select one to learn or take a quiz.
    During the quiz, select answers for each question. Your score will be shown at the end.
    Check your profile to view your username and email.

---

##✅ Notes

    Quiz questions are randomized for each session.
    No feedback is provided on individual questions until the quiz ends.
    Images for questions are stored in static/images/ folder, organized by quiz.

---

##📌 License

This project is for educational purposes and part of personal learning.
Feel free to fork and adapt for your own projects.

This version **preserves all formatting** on GitHub:  
- Blue for code blocks (`bash` or `text`)  
- Proper headings (`##`, `###`)  
- Bullets and indentation intact  

---