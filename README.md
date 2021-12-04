
THIS README IS OUT OF DATE AND IS CURRENTLY UNDER CONSTRUCTION

About The Project

Built With

Getting Started

Installation and Setup

Usage

	The flask application is now running on local port 5000. You can use the application by entering the following URI into your browser...

		localhost:5000

	Zip Code Validation

		The application comes preloaded with a mongodb database that
		runs on port 27017. This database is initialized when the app is run. The application uses a collection named "zipcodes". 

		If the "zipcodes" collection is not found, the application will repopulate the database using the raw text file. Please note: 			repopulating the database will take some time - attempting to use the server during database population may render a HTTP 503 status 		     code. If this happens, try again after a minute.

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
