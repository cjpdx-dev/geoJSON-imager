
# Flask imports
from flask import Flask
from flask import render_template, flash, redirect, request, jsonify, session, make_response
from flask import send_file, send_from_directory, safe_join, abort

from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Flask app imports
from app import app
from app import db_driver
from mongo_driver import AtlasUserWriteException, AtlasUserReadException

# FlaskForm imports
from app.forms import LoginForm
from app.forms import CreateAccountForm

# Python stdlib imports
import urllib.request
import requests
import json
import os
import codecs
import io

# For command line debugging
import pdb


@app.route('/')
@app.route('/index')
def index():
	print("calling index()")
	return render_template('index.html', title='Home')


@app.route('/mapView', methods=['GET', 'POST'])
def map_view():
	# TODO: Use secure filename and other security protocol before uploading file to server

	uploaded_file = request.files['file']

	if uploaded_file.filename != '' and '.geojson' in uploaded_file.filename:
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
		uploaded_file.save(file_path)
		
		try:
			opened_file = open(file_path, "r")
			
			try:
				jsonify(opened_file.read())
			
			# TODO: create custom exception for json.loads/json parasing error
			except Exception as e:
				print("GeoJSON data corrupted! Please choose a different file.")
				print(e)
				return redirect('/index')
		
		except FileNotFoundError as e:
			print(e)
			return redirect('/index')

		print("rendering mapView.html template")
		return render_template('mapView.html', title='View Map', file_name=uploaded_file.filename)

	else:
		flash("Something went wrong. Please select a .geoJSON file")
		return redirect('/index')


@app.route('/getGeoJSON', methods=['GET'])
def get_geo_json():
	try:
		file_name = request.args.get("fileName")
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
		
		opened_json = open(file_path, "r")
		read_json = opened_json.read()

		loaded_json = json.loads(read_json)

		return jsonify(loaded_json)

	except FileNotFoundError as e:
		print(e)
		return redirect('/index')

# TODO: Implement /location using async
# TODO: I should implement the call to Alyssa's service on the front end in mapView.html as
# I'm starting to not see any reason to use a /location route for this. For now I will just
# need to pass the uploaded file through again a second time when /location is called.
@app.route('/location', methods=['GET'])
def get_location_data():

	# TODO: see above todo: this is a stopgap messure for getting the originally uploaded file 
	# path to carry over to the re-rendered page so that we don't get a invalid key error in the
	# /mapView endpoint
	current_view_file_name = request.args.get("file-name")

	zip = request.args.get('zipcode')
	api_address = "http://localhost:8000/location?zip={}".format(zip)
	print(api_address)

	# ??? use requests or python native urllib.request.urlopen(url)?
	location_response = requests.get(api_address)
	print(location_response)

	if location_response:
		location_data = location_response.json()
		# print(location_data)

		flash("Feels Like: " + str(location_data["weather"]["current"]["main"]["feels_like"]) + " degrees Fahrenheit")
	
	return render_template('mapView.html', title="View Map", file_name=current_view_file_name)


@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	
	create_form = CreateAccountForm()
	
	if request.method == 'GET':
			return render_template('createAccount.html', title='Create Account', form=create_form)
	else:
		if create_form.validate_on_submit():

# 			# !!! Security vulnerability - raw passwords are being sent to SSO service through request form data
			# !!! Implemented SSL before release

			sso_service_response = requests.post('http://localhost:3000/create', json=request.form)
			print(sso_service_response)
			if sso_service_response:
				
				if sso_service_response.status_code == 200:

					try:
						db_driver.post_user(request.form.get("username"), 
											request.form.get("firstName"),
											request.form.get("lastName"),
											request.form.get("zipCode")
						)
						flash('Account Created - Please Login')
						return redirect('/login')

					except AtlasUserWriteException as e:
						print(e)
						flash("Database Error: Account Creation Failed. Please Try Again Later.")
				
				elif sso_service_response.status_code == 418:
					flash('Username already exists - please choose a different username and try again.')
				
				else:
					flash(str(sso_service_response.status_code) + 'Service Error: Account Creation Failed - An unknown error occured. Please try again later.')
			else:
				flash('Service Error: no response received from single sign on service')
		
		return render_template('createAccount.html', title="Create Account", form=create_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if request.method == 'GET':
			return render_template('login.html', title='Login', form=form)
	else:
		if form.validate_on_submit():
			
			sso_service_response = requests.post('http://localhost:3000/login', json=request.form)
			
			# !!! Security vulnerability - raw passwords are being received from SSO service through request form data.
			# !!! Implemented SSL before release
			
			if sso_service_response and sso_service_response.status_code == 200:
				
				try:
					user_data = db_driver.get_user(request.form.get("username"))
					print(user_data)
					if user_data["user_found"] is True:
						flash("Hi " + user_data["firstName"])
						return render_template('profile.html', title='Profile', user_details=user_data)
					else:
						flash('Account not found.')
						return render_template('login.html', title='Login', form=form)
				
				except AtlasUserReadException as e:
					print(e)
					flash('Database Error: Please Try Again Later')
					return render_template('login.html', title='Login', form=form)

		flash('Invalid Username or Password: Please Try Again')
		return render_template('login.html', title='Login', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():

	if request.method == 'GET':
		
		return render_template('profile.html', title="Profile")

# My service
@app.route('/validate_zip', methods=['GET'])
def validate_zip():
	
	zipcode_query = request.args.get('zipcode')
	payload = db_driver.find_zipcode(request.args.get('zipcode'))
	response = jsonify(payload)
	response.headers.add("Access-Control-Allow-Origin", "*")
	return response
