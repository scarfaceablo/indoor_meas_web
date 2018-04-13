from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DatePicker_start_day(FlaskForm):
    dt = DateField('DatePicker_start_day', format='%Y-%m-%d')
    dt2 = DateField('DatePicker_end_day', format='%Y-%m-%d')



    