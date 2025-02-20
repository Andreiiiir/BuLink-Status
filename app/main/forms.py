from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class CollabForm(FlaskForm):
    type_ = StringField('Type', validators=[DataRequired(), Length(min=3, max=25)])
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    particularities = StringField('Description', validators=[DataRequired(), Length(min=0, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    othercontact = StringField('Other Contact', validators=[DataRequired(), Length(min=3, max=50)])


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    particularities = StringField('Description', validators=[DataRequired(), Length(min=0, max=150)])
    pcollaborators = StringField('Collaborators', validators=[DataRequired(), Length(min=0, max=150)])
    status = SelectField('Status', choices=[('ACTIVE','ACTIVE'),('INACTIVE','INACTIVE')], validators=[DataRequired()])
