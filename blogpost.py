import os
from flask import Flask, render_template, request, redirect, Blueprint, flash, url_for
from werkzeug.utils import secure_filename
from forms import PostForm
from init_app import db, app
from model import Posts

blogpost = Blueprint('blogpost', __name__)

# Showing the blog post with the one
@blogpost.route('/post/<int:post_id>')
def show_post(post_id):
    active_page = 'explore'
    post = Posts.query.get_or_404(post_id)
    return render_template('posts.html', post=post, active_page=active_page)

# Edit the blog post again
@blogpost.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)
    form = PostForm()

    if form.validate_on_submit():
        # Check if there are changes in the form data
        if (
                form.image.data
                or form.title.data != post.title
                or form.content.data != post.content
                or form.author.data != post.author
                or form.description.data != post.description
                or form.slug.data != post.slug
        ):
            # Changes detected, proceed with updating
            # Check if a new image is provided
            if form.image.data:
                # Handle file upload
                image = form.image.data
                filename = secure_filename(image.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(file_path)
                # Update the post's image_path
                post.image_path = file_path

            # Update other form fields
            post.title = form.title.data
            post.content = form.content.data
            post.author = form.author.data
            post.description = form.description.data
            post.slug = form.slug.data

            # Update Database
            db.session.commit()
            flash('Post has been updated successfully!', 'success')
            return redirect(url_for('blogpost.show_post', post_id=post.id))
        else:
            # No changes, display a flash message
            flash('No changes made to the post.', 'info')
            return redirect(url_for('blogpost.show_post', post_id=post.id))

    # Pre-fill form data
    form.image.default = post.image_path
    form.title.data = post.title
    form.slug.data = post.slug
    form.author.data = post.author
    form.description.data = post.description
    form.content.data = post.content

    return render_template('edit_post.html', form=form, post=post, active_page='explore')

@blogpost.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post_to_delete = Posts.query.get_or_404(post_id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        # Return the message to remind
        flash('Blog has been deleted successfully!', 'success')

        # Grab all the posts from the database
        post = Posts.query.get_or_404(post_id)
        return render_template('posts.html', post=post, active_page='explore')

    except:
        # Return a error message
        flash("Whoops! There was a problem deleting blog post, try again later!", "alert")
        # Grab all the posts from the database
        post = Posts.query.get_or_404(post_id)
        return render_template('posts.html', post=post, active_page='explore')