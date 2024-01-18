from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def home():
    active_page = 'home'
    return render_template('home.html', active_page=active_page)


@app.route('/about')
def about():
    active_page = 'about'
    return render_template('about.html', active_page=active_page)


@app.route('/contact')
def contact():
    active_page = 'contact'
    return render_template('contact.html', active_page=active_page)

@app.route('/explore')
def explorer():
    active_page = 'explore'
    return render_template('explore.html',active_page=active_page)

@app.route('/blog_post_1')
def blog_post_1():
    active_page = 'explore'
    return render_template('blog_post_1.html',active_page= active_page)

@app.route('/blog_post_2')
def blog_post_2():
    active_page = 'explore'
    return render_template('blog_post_2.html', active_page=active_page)

if __name__ == '__main__':
    app.run(debug=True)
