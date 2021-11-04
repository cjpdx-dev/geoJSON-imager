from flask import Flask, render_template, flash, redirect, request, jsonify, session
from flask_restful import Resource, Api
from werkzeug.exceptions import HTTPException

from app import app
from app import db

from app.forms import LoginForm
from app.forms import CreateAccountForm

import urllib.request
import json
import os


# Documentation
#
#
#
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')


# Documentation
#
#
#
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	uploaded_file = request.files['file']
	
	if uploaded_file.filename != '' and '.geojson' in uploaded_file.filename:
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
		uploaded_file.save(file_path)

		# payload = {'file uploaded': 'true', 'file_path': file_path}
		# response = jsonify(payload)
		return redirect('/mapView')

	else:
		flash("Error: Please select a .geoJSON file.")
		return redirect('/index')

# Documentation
#
#
#
@app.route('/mapView', methods=['GET'])
def map_view():
	# TODO: need to pass the geoJSON file (or just the geoJSON file name) to mapView
	# when redirecting from /upload or /profile

	return render_template('mapView.html', title='View Map')

# Documentation
# placeholder route for Alyssa's microservice
#
#
@app.route('/location', methods=['GET'])
def get_location_data():
	flash("Current Weather: Sunny")
	flash("Population: 8.982 million" )
	# TODO: need to just update the page, not call a seperate route and render mapView.html again
	# which refreshes the mapView page and reloads the map, which will lead to user losing data
	return render_template('mapView.html', title="View Map")


# Documentation
#
#
#
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if request.method == 'GET':
			return render_template('login.html', title='Login', form=form)
	
	else:
		if form.validate_on_submit():

			if get_sso_service(form) is True:
				flash('Login Successful')
				return redirect('/profile')

		flash('Invalid Username or Password: Please Try Again')
		return render_template('login.html', title='Login', form=form)


# Documentation
# Placeholder GET from melissa's SSO service
#
#
def get_sso_service(form_data):
	# url = melissa's url + form_data with or without api_key (use os.environ.get("API_KEY"))
	# response = urllib.request.urlopen(url)
	# data = response.read()
	# dict = json.loads(data)
	sso_success = True

	if sso_success:
		return True
	else:
		return False
	 

# Documentation
#
#
#
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	
	form = CreateAccountForm()
	if request.method == 'GET':
			return render_template('createAccount.html', title='Create Account', form=form)
	else:
		if form.validate_on_submit():
			if post_sso_service(form) is True:
				flash('Account Created - Please Login')
				return redirect('/login')

		flash('Account Creation Failed: Please Try Again')
		return render_template('createAccount.html', title="Create Account", form=form)


# Documentation
# placeholder POST to Melissa's Single Sign On API
#
#
def post_sso_service(form):
	# url = melissa's url + form_data with or without api_key (use os.environ.get("API_KEY"))
	if form:
		sso_success = True
	else:
		sso_success = False

	if sso_success:
		return True
	else:
		return False


# Documentation
#
#
#
@app.route('/profile', methods=['GET', 'POST'])
def profile():

	if request.method == 'GET':
		return render_template('profile.html', title="Profile")


# My service
#
#
#
@app.route('/validate_zip', methods=['GET'])
def validate_zip():
	zipcode_query = request.args.get('zipcode')
	query_result = db.zipcodes.find_one({"_id": zipcode_query})
	
	if query_result:
		payload = {"valid_zip": True, "city": query_result["city"], "state": query_result["state"] }
	else:
		payload = {"valid_zip": False, "city": "", "state": "" }
	
	return jsonify(payload)



# # TODO: Remove this end point before migrating to a production server!
# def shutdown_server():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()

# @app.route('/shutdown', methods=['GET'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'
