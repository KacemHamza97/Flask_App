import json
import os

from flask import render_template, redirect, url_for, request, current_app
from flask import Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from web_app import db, login_manager
from web_app.admin_dashbord.forms import LoginForm, CreateAccountForm, AlgorithmSettings
from web_app.models import User

admin = Blueprint('admin', __name__, template_folder='templates/admin_dashbord', static_folder='static')


@admin.route('/route_default')
def route_default():
    return redirect(url_for('admin.login'))


@admin.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

@admin.route('/page-user')
def user():
    return render_template('page-user.html')



@admin.route('/index')
@login_required
def index():
    return render_template('index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.login'))

        # Something (user or pass) is not ok
        return render_template('login/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template('login/login.html', form=login_form)
    return redirect(url_for('admin.index'))


@admin.route('/create_user', methods=['GET', 'POST'])
def create_user():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('login/register.html', msg='Username already registered', form=create_account_form)

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('login/register.html', msg='Email already registered', form=create_account_form)

        # else we can create the user
        user = User(email, username, password)
        db.session.add(user)
        db.session.commit()

        return render_template('login/register.html', msg='User created please <a href="/login">login</a>',
                               form=create_account_form)

    else:
        return render_template('login/register.html', form=create_account_form)


@admin.route("/tables", methods=['GET', 'POST'])
def tables():
    form = AlgorithmSettings()
    if form.validate_on_submit():
        d = {'SQ':form.SQ.data, 'MCN': form.MCN.data, 'CP': form.CP.data, 'SN': form.SN.data,'SCP':form.SQ.data,'N':form.N.data}
        filepath = os.path.join(current_app.root_path, "static/files/admin_settings", "parameters.json")
        with open(filepath, 'w') as f:
            json.dump( d,f)
            return redirect(url_for('admin.index'))
    return render_template('tables.html', form=form)


@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/403.html'), 403


@admin.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403


@admin.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@admin.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500



# @admin.route('/<template>')
# def route_template(template):
#     if not current_user.is_authenticated:
#         return redirect(url_for('admin.login'))
#
#     try:
#
#         return render_template(template + '.html')
#
#     except TemplateNotFound:
#         return render_template('page-404.html'), 404
#
#     except:
#         return render_template('page-500.html'), 500
