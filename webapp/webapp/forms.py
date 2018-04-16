from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, NumberRange, Required

from webapp.models import User
from datetime import datetime
from datetime import timedelta

from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Register")


	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

class DatePicker_start_day(FlaskForm):
    dt = DateField('DatePicker_start_day', format='%Y-%m-%d', default=datetime.today()-timedelta(days=1))
    dt2 = DateField('DatePicker_end_day', format='%Y-%m-%d', default=datetime.today())

class MakeCallButton(FlaskForm):
	pin = PasswordField('Pin', validators=[DataRequired()])
	makecallbutton = SubmitField("make call")


class MapSamples(FlaskForm):
	mapsample=IntegerField("", validators=[NumberRange(min=1, max=20)])


class RatSelect(FlaskForm):
    rat = [(1,'GSM'),(2,'UMTS'),(3,'LTE'),(4,"all")]
    ratselect = SelectField('Technology', choices = rat)



		


    