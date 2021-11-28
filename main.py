import os

from flask import Flask, render_template, request, redirect, url_for, flash

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash # Flask login
from flask_login import LoginManager, login_user, current_user, login_required

app = Flask(__name__)

# SQLAlchemy stuff. Setup PostgreSQL databasee
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://xmxcxgpzeokbkp:8ea257b512ff268ebbd5475687c56236fd736c7d42e09439d89356ea7cf95906@ec2-3-230-199-240.compute-1.amazonaws.com:5432/d5gcfo146dri26').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # NOTE: Avoids error. Weird artifact of Flask.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '') # Needed for production Flask applications.

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import ProgressRecord, Course, User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Flask-admin stuff
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean' # set optional bootswatch theme
admin = Admin(app, name='RISE ABOVE Admin', template_mode='bootstrap4')
# -- Registering Flask-admin administrative views
admin.add_view(ModelView(ProgressRecord, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(User, db.session))


# Routes and views...

@app.route("/")
def home(name=None):
    """
    The RISE ABOVE home page.
    """

    return render_template('home.html', name=name)

from data_analysis import create_progress_chart
@app.route("/progress-dashboard", methods=['GET'])
@login_required
def progress_dashboard(name=None):
    """
    Dashboard view for showing user's progress over time.
    """
    # TODO: Query database, built dataframe build plot and visualize.
    plot = create_progress_chart(current_user, db)
    return render_template('progress_dashboard.html', plot=plot)


@app.route("/rating", methods=['GET', 'POST'])
@login_required
def rating(name=None):
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
        record = ProgressRecord(user_id=current_user.id, stress_rating=stress_rating,
                                positive_thinking_rating=positive_thinking_rating,
                                recognize_stigma_rating=recognize_stigma_rating,
                                problem_solving_rating=problem_solving_rating)

        # Add the record to the database
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('progress_dashboard')) # TODO: Switch to progress dashboard view.
        
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

    patient = current_user # NOTE: Use this to determine the order of effective each course should be to the patient.
    
    # TODO: Get the courses in order of applicability based on the patient's latest rating.

    return render_template('course_list.html', context={'courses':courses})


@app.route("/courses")
@login_required
def courses():
    """
    The page for rendering a particular course.
    """
    return render_template('courses.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup page. 
    NOTE: Inspired by: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
    """
    if request.method == 'POST':
            
        # code to validate and add user to database goes here
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Account with this email address already exists')
            return redirect(url_for('signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        login_user(user, remember=remember)
        return redirect(url_for('rating')) # User just created a new account. Need initial rating.

    # User wants to GET the signup page, so we just render the template
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    The page for the user to log in to the RISE ABOVE site.
    NOTE: Inspired by: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
    """
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('course_list'))

    # User wants to GET the login page, so we just render the template
    return render_template('login.html')
