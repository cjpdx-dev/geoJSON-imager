from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

# # imports for CLI command implementation
# import click
# from flask.cli import AppGroup

from config import Config
import db_scripts


app = Flask(__name__)
app.config.from_object(Config)

# TODO: add a CLI command to flask CLI for migrating/repopulating zipcodes db
# see: https://flask.palletsprojects.com/en/2.0.x/cli/

mongodb_client = PyMongo(app)
db = mongodb_client.db


db_scripts.repopulate_db(mongodb_client)

from app import routes
