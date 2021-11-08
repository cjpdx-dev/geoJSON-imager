from flask import Flask, render_template, flash, redirect, request, jsonify, session

from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app import app
from app import db_driver

from app.forms import LoginForm
from app.forms import CreateAccountForm

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

import urllib.request

import requests
import json
import os

_executor = ThreadPoolExecutor(1)

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
# Placeholder route for Alyssa's microservice
# If we want to try to do this with async later...
# ??? https://stackoverflow.com/questions/49822552/python-asyncio-typeerror-object-dict-cant-be-used-in-await-expression
# ??? https://stackoverflow.com/questions/33357233/when-to-use-and-when-not-to-use-python-3-5-await/33399896#33399896
# use app.before_request() and after_request() to handle thread/loop creation?
@app.route('/location', methods=['GET'])
def get_location_data():

	api_address = "http://localhost:3000/location?zip={}".format(request.args.get("zipcode"))
	
	# ??? use requests or python native urllib.request.urlopen(url)?
	location_response = requests.get(api_address)

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
# 			# ASK: Melissa if she is planning on using any type of encryption via certs or sessions
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
			
			if get_sso_service(form) is True:
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
