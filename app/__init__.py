
from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

# # imports for CLI command implementation
# import click
# from flask.cli import AppGroup

from config import Config
import db_scripts as db_scripts

# os imports
import atexit


app = Flask(__name__)
app.config.from_object(Config)

# TODO: add a CLI command to flask CLI for migrating/repopulating zipcodes db
# see: https://flask.palletsprojects.com/en/2.0.x/cli/
# or, just ignore this and drop the table each time the app is shutdown

mongodb_client = PyMongo(app)
db = mongodb_client.db

if "zipcodes" not in db.list_collection_names():
    print("creating collection \"zipcodes\" ")
    db.create_collection("zipcodes")

    db_scripts.create_zipcodes_db(mongodb_client)


from app import routes


