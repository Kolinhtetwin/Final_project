from flask import Blueprint, render_template, flash, redirect, url_for
from forms import PostForm
from init_app import db, app
from model import Posts
from werkzeug.utils import secure_filename
import os

add_post = Blueprint('add_post', __name__)


@add_post.route('/add_post', methods=['GET', 'POST'])
def upload_post():
    form = PostForm()
    if form.validate_on_submit():

        # check the photo is uploaded or not
        if form.image.data:
            # Handle file upload
            image = form.image.data
            filename = secure_filename(image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(file_path)
        else:
            # Handle case where no image is provided
            flash('No image file provided.', 'error')
            # Redirect or render an error message as needed
            return redirect(url_for('add_post.upload_post'))
        # upload the data to database
        posts = Posts(title=form.title.data, content=form.content.data,
                      image_path=file_path, author=form.author.data,
                      description=form.description.data, slug=form.slug.data)
        # Clear the Form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Add post data to database
        db.session.add(posts)
        db.session.commit()

        # Return a Message
        flash('Your blog post has been added!', 'success')
        return redirect(url_for('home.home_route'))

    # Redirected to the webpage
    return render_template('add_post.html', form=form)




