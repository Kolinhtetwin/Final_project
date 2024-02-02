import logging
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

from init_app import db, app
from model import User, Profile
from forms import LoginForm, RegistrationForm, ProfileEditForm, ProfileForm

login_manage = Blueprint('login_manage', __name__)



@login_manage.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():

            user = User(email=form.email.data, user_type=form.user_type.data, password=form.password.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Congratulations, you are now a registered user!')
            # Redirect to profile completion page after registration
            return redirect(url_for('login_manage.complete_profile'))
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template('register.html', title='Register', form=form)


@login_manage.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            # Handle file upload
            image = form.profile_pic.data
            filename = secure_filename(image.filename)
            profile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(profile_path)

            print(f"Filename: {filename}")
            print(f"Profile Path: {profile_path}")
        else:
            profile_path = os.path.join(app.config['UPLOAD_FOLDER'], 'default_profile_pic.jpeg')
            print(f"Default Profile Path: {profile_path}")
        full_profile = Profile(user_id=current_user.id, profile_pic=profile_path, username=form.username.data, age=form.age.data,
                               gender=form.gender.data, dob=form.dob.data)
        db.session.add(full_profile)
        db.session.commit()
        flash('Profile completed successfully!')
        return redirect(url_for('login_manage.profile'))
    return render_template('fill_profile.html', title='Complete Profile', form=form)


@login_manage.route('/login_route', methods=['GET', 'POST'])
def login_route():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        try:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('Logged in successfully')

                # Check if the user has filled out the profile
                if not user.has_filled_profile():
                    return redirect(url_for('login_manage.complete_profile'))

                next = request.args.get('next')

                if next is None or not next[0] == '/':
                    next = url_for('login_manage.profile')  # Set a default route

                return redirect(next)
            else:
                flash("Incorrect Password!")
                return redirect(url_for('login_manage.login_route'))
        except AttributeError:
            flash("Email doesn't exist. Kindly register.")
            return redirect(url_for('login_manage.login_route'))

    return render_template('login.html', form=form)


# LogOut
@login_manage.route('/logout_route', methods=['GET', 'POST'])
@login_required
def logout_route():
    logout_user()
    flash('You have been logged out! Thanks for using our web-application')
    return redirect(url_for('home.home_route'))


# Go to Profile page after Login
@login_manage.route('/profile')
@login_required
def profile():
    # Assuming there's a one-to-one relationship between User and Profile
    user_profile = Profile.query.filter_by(user_id=current_user.id).first()

    if user_profile:
        # Extracting data from the profile
        user_name = user_profile.username
        dob = user_profile.dob
        age = user_profile.age
        gender_display = "Male" if user_profile.gender == "M" else "Female"
        disease_list = current_user.diseases

        # Extracting symptoms, disease names, descriptions, and precautions
        symptoms_list = [disease.symptoms for disease in disease_list]
        disease_name_list = [disease.disease_name for disease in disease_list]
        disease_description_list = [disease.get_disease_descriptions() for disease in disease_list]
        precaution_list = [disease.get_precautions() for disease in disease_list]

        # Zipping the lists to create a dictionary
        disease_dict = {
            'symptoms': symptoms_list,
            'disease_name': disease_name_list,
            'disease_description': disease_description_list,
            'precaution': precaution_list,
        }

        return render_template('profile.html', gender_display=gender_display, user_name=user_name,
                               age=age, dob=dob, disease_dict=disease_dict, active_page='profile')
    else:
        # Handle the case where the profile doesn't exist for the current user
        flash("Profile not found. Please complete your profile.")
        return redirect(url_for('login_manage.complete_profile'))


@login_manage.route('/profile/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = ProfileEditForm()

    if form.validate_on_submit():

        # Check if there are changes in the form data
        if (
                form.profile_pic.data
                or form.username.data != user.profile.username
                or form.email.data != user.email
                or form.dob.data != user.profile.dob
                or form.age.data != user.profile.age
                or form.gender.data != user.profile.gender
        ):
            # Check if a new image is provided
            if form.profile_pic.data:
                # Handle file upload
                image = form.profile_pic.data
                filename = secure_filename(image.filename)
                profile_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(profile_path)
                # Update the post's image_path
                user.profile.profile_pic = profile_path

            # Changes detected, proceed with updating
            user.profile.username = form.username.data
            user.email = form.email.data
            user.profile.dob = form.dob.data
            user.profile.age = form.age.data
            user.profile.gender = form.gender.data
            # Update Database
            db.session.commit()
            flash('Profile has been updated successfully!', 'success')
            return redirect(url_for('login_manage.profile', user_id=user.id))
        else:
            # No changes, display a flash message
            logging.info("No changes made to the profile.")
            flash('No changes made to the profile.', 'info')
            return redirect(url_for('login_manage.profile', user_id=user.id))

    # Pre-fill form data
    form.username.data = user.profile.username
    form.email.data = user.email
    form.dob.data = user.profile.dob
    form.age.data = user.profile.age
    form.gender.data = user.profile.gender

    return render_template('edit_profile.html', form=form, user_id=user_id, active_page='profile')
