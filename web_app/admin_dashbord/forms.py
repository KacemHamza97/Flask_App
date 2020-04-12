from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired


# login and registration

class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired()])
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()])
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()])


class AlgorithmSettings(FlaskForm):
    SQ = StringField('SQ', id='SQ', validators=[DataRequired()])
    MCN = StringField('MCN', id='MCN', validators=[DataRequired()])
    CP = StringField('CP', id='CP', validators=[DataRequired()])
    SN = StringField('SN', id='SN', validators=[DataRequired()])
    submit = SubmitField('Set Parameters')

