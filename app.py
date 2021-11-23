from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# Setup SQL databasee
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Model schema

class Course(db.Model):
    """
    Attributes:
        Name
        Photo
        Description
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # photo = db.Column(db.Photo, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __str__(self):
        return self.name


class Video(db.Model):
    """
    Attributes:
        Title
        Link to video, or video file
        Course (relationship)
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(150), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref=db.backref('videos', lazy=True))

    def __str__(self):
        return self.title


class ProgressRecord(db.Model)
    """
    Attributes:
        Date/time
        Stress rating
        Positive thinking rating
        Recognizing stigma rating
        Problem solving rating
        User
    """
    date_taken = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    stress_rating = db.Column(db.Integer, nullable=False)
    positive_thinking_rating = db.Column(db.Integer, nullable=False)
    recognize_stigma_rating = db.Column(db.Integer, nullable=False)
    problem_solving_rating = db.Column(db.Integer, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', backref=db.backref('progress_records', lazy=True))


@app.route("/")
def home(name=None):
    """
    The RISE ABOVE home page.
    """
    return render_template('home.html', name=name)


@app.route("/rating")
def rating(name=None):
    """
    Page for the user to rate themself.
    """
    return render_template('rating.html', name=name)


@app.route("/courses")
def hello_world(name=None):
    """
    The RISE ABOVE home page.
    """
    return render_template('course_home.html', name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    The page for the user to log in to the RISE ABOVE site.
    """
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)