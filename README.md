About The Project

Built With

Getting Started

	Prerequisites: 
		pip
		Python Version 3.7.6

Installation and Setup

	Step 1: Navigate to your preferred installation directory and use the command...

		git clone https://github.com/cjpdx-dev/geoJSON-imager


	Step 2: Navigate into the installation directory /geoJSON-imager


	Step 3: Once inside the installation directory, run the following commands...

		python3 -m venv venv

		source venv/bin/activate

		pip install -r requirements.txt

	Step 4: Exit the current terminal session and open a new termianl session. Navigate back to the geoJSON-imager directory
	and run the following command again...

		source venv/bin/activate

	Step 5: Start the flask server using the command...

		flask run

Usage

	The flask application is now running on local port 5000. You can use the application by entering the following URI into your browser...

		localhost:5000

	Zip Code Validation

		The application comes preloaded with a mongodb database that
		runs on port 27017. This database is initialized when the app is run. The application uses a collection named "zipcodes". 

		If the "zipcodes" collection is not found, the application will repopulate the database using the raw text file. Please note: repopulating the database will take some time - attempting to use the server during database population may render a HTTP 503 status code. If this happens, try again after a minute.

		---------------------------------------------------------------------------------

		To use the application's zip code validation service, send a GET request with a zipcode parameter using the following format:

			localhost:5000/validate_zip?zipcode=19804

		Using this request example, the following JSON will be generated as a response:

			{
  				"city": "Wilmington", 
  				"state": "DE", 
  				"valid_zip": true
			}

		In the case of an invalid zipcode, the following response format will be used:

			{
  				"city": "", 
  				"state": "", 
  				"valid_zip": false
			}

Roadmap

Contributing

License

Contact

Acknowledgments