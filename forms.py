from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField, IntegerField
from wtforms.fields.choices import RadioField
from wtforms.fields.datetime import DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length
from wtforms import ValidationError
from wtforms.widgets import TextArea
from model import User, Profile
from flask_ckeditor import CKEditorField


class ProfileForm(FlaskForm):
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = Profile.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    user_type = RadioField('User Type',
                           choices=[('user', 'Regular User'), ('healthcare_professional', 'Healthcare Professional')],
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Enter Email:', validators=[DataRequired('Kindly Enter Your Email!'), Email()])
    password = PasswordField('Enter Password:', validators=[DataRequired('Enter Your Password!')])
    submit = SubmitField('Log In')


class PostForm(FlaskForm):
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProfileEditForm(FlaskForm):
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'],
                                                                       'Images only!')])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[('M', 'Male'), ('F', 'Female')])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')
