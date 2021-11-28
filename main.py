import os

from flask import Flask, render_template, request, redirect, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# SQLAlchemy stuff. Setup PostgreSQL databasee
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://xmxcxgpzeokbkp:8ea257b512ff268ebbd5475687c56236fd736c7d42e09439d89356ea7cf95906@ec2-3-230-199-240.compute-1.amazonaws.com:5432/d5gcfo146dri26').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # NOTE: Avoids error. Weird artifact of Flask.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '') # Needed for production Flask applications.

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import ProgressRecord, Course

# Flask-admin stuff
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean' # set optional bootswatch theme
admin = Admin(app, name='RISE ABOVE Admin', template_mode='bootstrap4')
# -- Registering Flask-admin administrative views
admin.add_view(ModelView(ProgressRecord, db.session))
admin.add_view(ModelView(Course, db.session))


@app.route("/")
def home(name=None):
    """
    The RISE ABOVE home page.
    """

    return render_template('home.html', name=name)


@app.route("/rating")
def rating(name=None, methods=['GET', 'POST']):
    """
    Page for the user to rate themself.
    """
    if request.method == 'POST':
        # Get the data from the form
        stress_rating = request.form.get('stress_rating')
        positive_thinking_rating = request.form.get('positive_thinking_rating')
        recognize_stigma_rating = request.form.get('recognize_stigma_rating')
        problem_solving_rating = request.form.get('problem_solving_rating')

        # Create a new record
        record = ProgressRecord(stress_rating=stress_rating,
                                positive_thinking_rating=positive_thinking_rating,
                                recognize_stigma_rating=recognize_stigma_rating,
                                problem_solving_rating=problem_solving_rating)

        # Add the record to the database
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('course_list'))
        
    elif request.method == 'POST':
        logged_in = False
        if not logged_in: # TODO: check if user is actually logged in here.
            return render_template('login.html', name=name)
            
    return render_template('rating.html', name=name)


@app.route("/course-list")
def course_list():
    """
    View for rendering the course list.

    NOTE: This should be sorted by the impact that the course is expected to have on the user.
    """
    courses = Course.query.all()
    return render_template('course_list.html', context={'courses':courses})


@app.route("/courses")
def courses():
    """
    The page for rendering a particular course.
    """
    return render_template('courses.html')


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
