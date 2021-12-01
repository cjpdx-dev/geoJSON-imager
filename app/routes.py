
# Flask imports
from flask import Flask
from flask import render_template, flash, redirect, request, jsonify, session, make_response
from flask import send_file, send_from_directory, safe_join, abort

from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Flask app imports
from app import app
from app import db_driver

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

# TODO: Documentation Needed
@app.route('/')
@app.route('/index')
def index():
	print("calling index()")
	return render_template('index.html', title='Home')


# # TODO: Implement /upload end point for logged in user to upload geoJSON
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
# 	print("calling upload_file()")
# 	uploaded_file = request.files['file']
# 	if uploaded_file.filename != '' and '.geojson' in uploaded_file.filename:
		
# 		file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
# 		uploaded_file.save(file_path)
		
# 		return redirect(urlfor('/mapView', file_path='file_path'))

# 	else:
# 		flash("Error: Please select a .geoJSON file.")
# 		return redirect('/index')

# TODO: Documentation Needed
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
				# uploaded_file_to_json = json.dumps(opened_file.read())
				# print(uploaded_file_to_json)
				# dumped_geojson = json.dumps(uploaded_file_to_json)

				# TODO: need to make the use of this header conditional, based on if the uploaded file
				# already has a populated title/type/data field
				# geojson_header["uploaded-map"]["data"] = uploaded_file_to_json
				# print("updated the geojson_header's data field")
			
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
		print("File Name: ", request.args.get("fileName"))
		file_name = request.args.get("fileName")
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
		
		opened_json = open(file_path, "r")
		read_json = opened_json.read()

		loaded_json = json.loads(read_json)
		print(loaded_json)
		print(type(loaded_json))

		return jsonify(loaded_json)
	except FileNotFoundError as e:
		print(e)
		return redirect('/index')

# Documentation
# If we want to try to do this with async later...
# ??? https://stackoverflow.com/questions/49822552/python-asyncio-typeerror-object-dict-cant-be-used-in-await-expression
# ??? https://stackoverflow.com/questions/33357233/when-to-use-and-when-not-to-use-python-3-5-await/33399896#33399896
# use app.before_request() and after_request() to handle thread/loop creation?
@app.route('/location', methods=['GET'])
def get_location_data():

	zip = request.args.get('zipcode')
	api_address = "http://localhost:3000/location?zip={}".format(zip)
	print(api_address)

	# ??? use requests or python native urllib.request.urlopen(url)?
	location_response = requests.get(api_address)
	print(location_response)

	if location_response:
		print("Recieved response from port 3000")
		print("current weather: ")
		location_data = location_response.json()

		flash("Current Weather: " + str(location_data["weather"]["current"]))
		flash("Five Day Forecast: " + str(location_data["weather"]["five_day"]))
	
	return redirect('/mapView')


# Documentation
#
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	
	create_form = CreateAccountForm()
	
	if request.method == 'GET':
			return render_template('createAccount.html', title='Create Account', form=create_form)
	else:
		if create_form.validate_on_submit():

# 			# !!! This is a major security vulnerability - change before migrating to production build
# 			# ASK: Melissa if she is planning on using any type of encryption via certs or sessions?
			response = requests.post('http://localhost:3000/create', json=request.form)
			
			if response:
				if response.status_code == 200:
					flash('Account Created - Please Login')
					return redirect('/login')
				
				elif response.status_code == 418:
					flash('Username already exists - please choose a different username and try again.')
				
				else:
					flash(str(response.status_code) + 'Sorry, an unknown error occured - your account was not created. Please try again later.')
			else:
				flash('Error: no response received from single sign on service')
		
		return render_template('createAccount.html', title="Create Account", form=create_form)

# Documentation
#
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	
	if request.method == 'GET':
			return render_template('login.html', title='Login', form=form)
	else:
		if form.validate_on_submit():
			
			response = requests.post('http://localhost:3000/login', json=request.form)
			
			# !!! This is a major security vulnerability - change before migrating to production build
# 			# ASK: Melissa if she is planning on using any type of encryption via certs or sessions
			
			if response and response.status_code == 200:
				flash('Login Successful')
				return redirect('/profile')

		flash('Invalid Username or Password: Please Try Again')
		return render_template('login.html', title='Login', form=form)

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
	payload = db_driver.find_zipcode(request.args.get('zipcode'))
	response = jsonify(payload)
	response.headers.add("Access-Control-Allow-Origin", "*")
	return response
