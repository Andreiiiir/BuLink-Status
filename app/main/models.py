from app import db
from app.auth.models import User

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    particularities = db.Column(db.String(150), nullable=False)
    pcollaborators = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)



class Collaborator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_ = db.Column(db.String(35), nullable=False)
    name = db.Column(db.String(35), nullable=False)
    particularities = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    othercontact = db.Column(db.String(50), nullable=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship back to User
    user = db.relationship('User', back_populates='notes')
    





