import json
from datetime import datetime
from init_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# loads the user according to their unique id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# user class for making new users, checking if passwords match
class User(db.Model, UserMixin):
    # this is the tablename inside the database
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    diseases = db.relationship('Disease', backref='users', lazy='dynamic')
    profile = db.relationship('Profile', backref='profiles', uselist=False)

    def __init__(self, email, user_type, password):
        self.email = email
        self.user_type = user_type
        # saving a sha sum hash instead of actual pass
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def diseases_dict(self):
        disease_list = []
        symptoms_list = []
        disease_des = []
        precaution = []
        for disease in self.diseases:
            disease_list.append(disease.disease_name)
            symptoms_list.append(disease.symptoms)
            disease_des.append(disease.disease_description)
            precaution.append(disease.precaution)
        disease_dict = dict(zip(symptoms_list, disease_list))
        return disease_dict

    def has_filled_profile(self):
        return self.profile is not None


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, user_id, profile_pic, username, dob, gender, age):
        self.user_id = user_id
        self.profile_pic = profile_pic
        self.username = username
        self.dob = dob
        self.gender = gender
        self.age = age


# diseases class
class Disease(db.Model):
    __tablename__ = 'diseases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    symptoms = db.Column(db.Text)
    disease_name = db.Column(db.Text)
    disease_description = db.Column(db.Text)
    precaution = db.Column(db.Text)

    def __init__(self, user_id, symptoms, disease_name, disease_description, precaution):
        self.user_id = user_id
        self.symptoms = symptoms
        self.disease_name = disease_name
        self.disease_description = disease_description
        self.precaution = json.dumps(precaution)

    def get_precautions(self):
        return json.loads(self.precaution)

    def get_disease_descriptions(self):
        return self.disease_description.split(" | ")


class Posts(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    slug = db.Column(db.String(255))
    image_path = db.Column(db.String(255))

    def __init__(self, title, content, author, description, slug, image_path):
        self.title = title
        self.content = content
        self.author = author
        self.description = description
        self.slug = slug
        self.image_path = image_path
