# NECESSARY IMPORTS FOR SETTING UP FLASK AND USER AUTH
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor

# SETTING UP LOGIN MANAGER AND FLASK APP
login_manager = LoginManager()
app = Flask(__name__)

# CREATING THE DATABASE CONFIGS
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Upload the image to the default file
app.config['UPLOAD_FOLDER'] = f'{basedir}/static/images'
ckeditor = CKEditor(app)


# DATABASE CREATED AND MIGRATE SET UP
db = SQLAlchemy(app)
Migrate(app, db)

# INITIALIZING LOGIN MANAGER
login_manager.init_app(app)

# WHICH FUNCTION WILL THE USER NEED TO SEE FOR LOGIN
login_manager.login_view = "login_route"