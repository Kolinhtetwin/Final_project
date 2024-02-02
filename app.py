# app.py
from home import home
from about import about
from contact_us import contact
from login import login_manage
from symptom_checker import symptom_checker
from init_app import app, db
from add_post import add_post
from blogpost import blogpost
from explore import explore

# Register blueprints for different parts of the website
app.register_blueprint(home)
app.register_blueprint(about)
app.register_blueprint(contact)
app.register_blueprint(login_manage)
app.register_blueprint(symptom_checker)
app.register_blueprint(add_post)
app.register_blueprint(blogpost)
app.register_blueprint(explore)

if __name__ == '__main__':
    app.run(debug=True)
