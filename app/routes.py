from flask import render_template, flash, redirect, request, jsonify
from app import app
from app.forms import LoginForm
from app.forms import CreateAccountForm

import os

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if form.validate_on_submit():
		
		flash('Login Successful')

		return redirect('/index')
	
	flash('Please Try Again')
	return render_template('login.html', title='Login', form=form)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	
	form = CreateAccountForm()

	if form.validate_on_submit():

		flash('Account Created')

		return redirect('/index')

	flash('Please Try Again')
	return render_template('createAccount.html', title="Create Account", form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
		uploaded_file.save(file_path)

		payload = {'file uploaded': 'true', 'file_path': file_path}
		response = jsonify(payload)
		return redirect('/mapView')

@app.route('/mapView', methods=['GET'])
def map_view():

	return render_template('mapView.html', title='View Map')





