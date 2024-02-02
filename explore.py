from flask import Blueprint, render_template, url_for

from model import Posts

explore = Blueprint('explore', __name__)


@explore.route('/explore')
def explore_route():
    active_page = 'explore'
    # Grab all posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("explore.html", posts=posts, active_page=active_page)
