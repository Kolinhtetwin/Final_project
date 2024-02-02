from flask import Flask, render_template, request, redirect, session, Blueprint, flash
from flask_login import current_user
from flask_wtf import form

import ml
from init_app import db
from model import Disease

symptom_checker = Blueprint('symptom_checker', __name__)


@symptom_checker.route('/symptom_checker')
def form1():
    symptom_list = ml.get_symptoms()
    ml.yes_or_no = []
    return render_template('symptom_checker.html', symptoms_list=symptom_list, active_page='symptom_checker')


@symptom_checker.route('/process_form1', methods=['POST'])
def process_form1():
    symptom = request.form.get('symptoms')
    num_days = int(request.form.get('s_day'))
    session['num_days'] = num_days
    clf, cols = ml.train()
    symptom_data = ml.tree_to_code(clf, cols, symptom)
    symptoms_label = [symptom.replace('_', ' ') for symptom in symptom_data]
    ml.yes_or_no = []
    ml.symptoms_exp = []
    return render_template('form2.html', symptoms=symptoms_label, current_symptom=symptoms_label[0],
                           remaining_symptoms=','.join(symptoms_label[1:]), active_page='symptom_checker')


@symptom_checker.route('/process_form2', methods=['POST'])
def process_form2():
    current_symptom = request.form.get('current_symptom')
    user_response = request.form.get('response')
    remaining_symptoms = request.form.get('remaining_symptoms')

    if user_response == 'yes':
        ml.yes_or_no.append('yes')

        if remaining_symptoms:
            # If there are remaining symptoms, update the current_symptom and go back to the form
            return render_template('form2.html', symptoms=remaining_symptoms,
                                   current_symptom=remaining_symptoms.split(',')[0],
                                   remaining_symptoms=','.join(remaining_symptoms.split(',')[1:]), active_page='symptom_checker')
        else:
            # If there are no remaining symptoms, display a success message
            return redirect('result')
    else:
        # Continue with your logic for handling 'no' response
        ml.yes_or_no.append('no')

        if remaining_symptoms:
            # If there are remaining symptoms, update the current_symptom and go back to the form
            return render_template('form2.html', symptoms=remaining_symptoms,
                                   current_symptom=remaining_symptoms.split(',')[0],
                                   remaining_symptoms=','.join(remaining_symptoms.split(',')[1:]), active_page='symptom_checker')
        else:
            # If there are no remaining symptoms, display a success message
            return redirect('result')


@symptom_checker.route('/result')
def result():
    ml.getDicts()
    ml.recurse2(session['num_days'])
    symptom_string = ml.list_to_string(ml.symptoms_exp)
    predicted_disease = ml.predicted_disease
    # Example storing process in your Flask route or view function
    combined_description = f"{ml.predicted_disease_description} | {ml.predicted_disease_description2}" \
        if ml.predicted_disease_description2 else ml.predicted_disease_description

    # Convert precaution_list to a set to ensure uniqueness
    unique_precaution_set = set(ml.precaution_list)

    # Check if ml.precaution_list2 is different from ml.precaution_list
    if ml.precaution_list2 and set(ml.precaution_list2) != unique_precaution_set:
        # Combine unique precaution lists
        combined_precaution = f"{', '.join(unique_precaution_set)} | {', '.join(ml.precaution_list2)}"
    else:
        # Use only the unique precaution_list
        combined_precaution = ', '.join(unique_precaution_set)

    print("Yes or No",ml.yes_or_no)
    print("Symptoms Exp",ml.symptoms_exp)
    if current_user.is_authenticated:
        if ml.yes_or_no == []:
            flash('Prediction Already Saved!')
        else:
            disease = Disease(
                user_id=current_user.id,
                symptoms=symptom_string,
                disease_name=ml.predicted_disease,
                disease_description=combined_description,
                precaution=combined_precaution
            )
            db.session.add(disease)
            db.session.commit()
            ml.yes_or_no = []
            flash('Prediction Saved!')
    return render_template("result.html", condition=ml.condition, color=ml.color,
                           precaution_list=ml.precaution_list,
                           predicted_disease=predicted_disease,
                           predicted_disease_description=ml.predicted_disease_description,
                           predicted_disease_description2=ml.predicted_disease_description2,
                           precaution_list2=ml.precaution_list2,
                           active_page= 'symptom_checker')
