# =============================================================================
# importing necessary libraries
# =============================================================================
from flask_login import UserMixin
from database import db

# =============================================================================
# User Password Table
# =============================================================================
class User(db.Model, UserMixin):
    __tablename__ = "User"
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    update = db.relationship('StatusUpload', backref="update", lazy=True)
    activity= db.relationship('activityStack', backref="activity", lazy=True)

# =============================================================================
# Status Upload(image only) table
# =============================================================================
class StatusUpload(db.Model):
    __tablename__ = "StatusUpload"
    picid=db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    img = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    
# =============================================================================
# past users table
# =============================================================================
class activityStack(db.Model):
    __tablename__ = "activityStack"
    actid=db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)