import json
import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, Blueprint, flash, current_app, session
from flask_login import login_user, current_user, logout_user

from web_app import db
from web_app.models import User
from web_app.users.back_end.generate import generate_solution
from web_app.users.file_handler import add_file, input_data
from web_app.users.forms import Login, Register, UploadFile, AlgorithmType

dev = Blueprint('dev', __name__, template_folder='templates/users', static_folder='static')


@dev.route('/')
def main():
    return render_template('main.html')


@dev.route('/submits', methods=['GET', 'POST'])
def submits():
    pathsub = os.path.join(current_app.root_path, f"static/files/users_uploads/{current_user.id}/submits")
    pathres = os.path.join(current_app.root_path, f"static/files/users_uploads/{current_user.id}/results")
    pathrelativesubmits = f"/static/files/users_uploads/{current_user.id}/submits/"
    pathrelativeresults = f"/static/files/users_uploads/{current_user.id}/results/"
    files_names_sub = os.listdir(pathsub)
    files_names_res = os.listdir(pathres)

    L1 = []  # date formated list
    for name in files_names_sub:
        format_date = name[:-5].replace('_', '-', 2).replace('_', ':', 2)
        L1.append((format_date, name))

    L2 = []  # date formated list
    for name in files_names_res:
        L2.append((name))

    return render_template('submits.html', L1=L1[::-1], L2=L2[::-1], pathrelativesubmits=pathrelativesubmits, pathrelativeresults=pathrelativeresults)


@dev.route('/result', methods=['GET', 'POST'])
def result():
    solution_services, final_solutions = generate_solution()
    data_j = input_data(solution_services)
    if current_user.is_authenticated:
        add_file(data_j, current_user, type="output")
        pathd = os.path.join(current_app.root_path, f"static/files/users_uploads/{current_user.id}/results")
        files_name = os.listdir(pathd)[-1]
        pathrelative = f"/static/files/users_uploads/{current_user.id}/results/" + files_name
    else:
        user = User(datetime.now(), "__@gmail.com", "-1")
        add_file(data_j, user, type="output")
        pathd = os.path.join(current_app.root_path, f"static/files/users_uploads/None/results")
        files_name = os.listdir(pathd)[-1]
        pathrelative = f"/static/files/users_uploads/None/results/" + files_name


    return render_template('result.html', solution_services=solution_services, final_solutions=final_solutions, pathrelative=pathrelative)


@dev.route('/service', methods=['GET', 'POST'])
def service():
    form = AlgorithmType()
    if form.validate_on_submit():
        if form.submit1.data:  # if submit1 is clicked
            session["algorithm"] = "Single-objective"
            return redirect(url_for('dev.upload'))
        if form.submit2.data:  # if submit2 is clicked
            session["algorithm"] = "Multi-objective"
            return redirect(url_for('dev.upload'))
    return render_template('service.html', form=form)


@dev.route("/client_logout")
def client_logout():
    logout_user()
    session.clear()
    return redirect(url_for('dev.service'))


@dev.route('/client_login', methods=['GET', 'POST'])
def client_login():
    form = Login()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            next = request.args.get('next')

            if form.username.data == 'Hamza':
                return redirect(url_for('admin.login'))

            elif next is None or not next[0] == '/':
                return redirect(url_for('dev.service'))

    return render_template('client_login.html', form=form)


@dev.route('/client_register', methods=['GET', 'POST'])
def client_register():
    form = Register()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('dev.client_login'))
    return render_template('client_register.html', form=form)


@dev.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadFile()
    if form.validate_on_submit():
        if form.file.data:
            if current_user.is_authenticated:
                user = current_user
                add_file(form.file.data, user)
                flash('File uploaded successfully')
            else:
                user = User(datetime.now(), "__@gmail.com", "-1")
                add_file(form.file.data, user)
                flash('File uploaded successfully')
        return redirect(url_for('dev.result'))
    return render_template('upload.html', form=form)
