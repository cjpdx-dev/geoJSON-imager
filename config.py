import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	UPLOAD_FOLDER = "local_data/uploads/"
	MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
	MONGO_URI = "mongodb+srv://cjpdx:OsY8rrimVnY6vmvB@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"
