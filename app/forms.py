from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	password= PasswordField('Password', validators=[DataRequired()])
	
	# not sure if I'm going to use these or not
	firstName = StringField('First name', validators=[DataRequired()])
	zipcode = IntegerField('Zip Code', validators=[DataRequired()])
	
	submit = SubmitField('Create Account')
