from datetime import datetime

from main import db

# Model schema

class Course(db.Model):
    """
    Attributes:
        Name
        Photo
        Description
    """
    course_id = db.Column(db.Integer, primary_key=True)
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
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    course = db.relationship('Course', backref=db.backref('videos', lazy=True))

    def __str__(self):
        return self.title


class ProgressRecord(db.Model):
    """
    Attributes:
        Date/time
        Stress rating
        Positive thinking rating
        Recognizing stigma rating
        Problem solving rating
        User
    """
    record_id = db.Column(db.Integer, primary_key=True)
    date_taken = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    stress_rating = db.Column(db.Integer, nullable=False)
    positive_thinking_rating = db.Column(db.Integer, nullable=False)
    recognize_stigma_rating = db.Column(db.Integer, nullable=False)
    problem_solving_rating = db.Column(db.Integer, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', backref=db.backref('progress_records', lazy=True))
