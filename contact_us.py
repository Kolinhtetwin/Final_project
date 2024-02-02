from flask import Blueprint, render_template, request
# from flask_mail import Mail, Message

contact = Blueprint('contact', __name__)


@contact.route('/contact')
def contact_us():
    active_page = 'contact'
    return render_template('contact.html', active_page=active_page)


@contact.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Do something with the data
    return "<script>alert('Thank you for your message, " + name + "!'); window.location.href='/contact';</script>"
