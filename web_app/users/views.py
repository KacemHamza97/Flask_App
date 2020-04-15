import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, Blueprint, flash, current_app

from flask_login import login_user, current_user, logout_user

from web_app import db
from web_app.models import User
from web_app.users.file_handler import add_file
from web_app.users.forms import Login, Register, UploadFile

dev = Blueprint('dev', __name__, template_folder='templates/users', static_folder='static')


@dev.route('/')
def main():
    return render_template('main.html')


@dev.route('/loading')
def loading():
    return render_template('loading_page.html')


@dev.route('/submits', methods=['GET', 'POST'])
def submits():
    pathd = os.path.join(current_app.root_path, f"static/files/users_uploads/{current_user.id}/submits")
    pathrelative = f"/static/files/users_uploads/{current_user.id}/submits/"
    files_names = os.listdir(pathd)
    L = []  # date formated list
    for name in files_names:
        format_date = name[:-5].replace('_', '-', 2).replace('_', ':', 2)
        L.append((format_date,name))

    return render_template('submits.html', L=L, pathrelative=pathrelative)


@dev.route('/service')
def service():
    return render_template('service.html')


# @dev.route('/upload')
# def upload():
#     return render_template("upload.html")


@dev.route("/client_logout")
def client_logout():
    logout_user()
    return redirect(url_for('dev.service'))


@dev.route('/client_login', methods=['GET', 'POST'])
def client_login():
    form = Login()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
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
        return redirect(url_for('dev.submits'))
    return render_template('upload.html', form=form)
