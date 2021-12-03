from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):

	username = StringField('Username: ', validators=[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])

	firstName = StringField('First name: ', validators=[DataRequired()])
	lastName = StringField('Last name:', validators=[DataRequired()])
	zipCode = StringField('Zip Code: ', validators=[DataRequired()])

	submit = SubmitField('Create Account')
