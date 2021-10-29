import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

	# placeholder for database - config the upload folder for map uploads
	# and specify max file size
	
	UPLOAD_FOLDER = "uploads/"
	MAX_CONTENT_LENGTH = 1024 * 1024 * 1024