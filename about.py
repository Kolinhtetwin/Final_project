from flask import Blueprint, render_template


about = Blueprint('about', __name__)

@about.route('/about')
def about_route():
    active_page = 'about'
    return render_template('about.html', active_page=active_page)
