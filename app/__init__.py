from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongodb_client = PyMongo(app)
db = mongodb_client.db

from app import routes


