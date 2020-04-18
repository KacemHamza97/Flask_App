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
    SCP = StringField('SQ', id='SCP',validators=[DataRequired()])
    SQ = StringField('SQ', id='SQ')
    MCN = StringField('MCN', id='MCN')
    CP = StringField('CP', id='CP',validators=[DataRequired()])
    SN = StringField('SN', id='SN')
    submit = SubmitField('Set Parameters')

