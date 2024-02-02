from flask import Blueprint, render_template,url_for


home = Blueprint('home', __name__)

@home.route('/')
def home_route():
    active_page= 'home'
    return render_template('home.html', active_page=active_page)
