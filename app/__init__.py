
from flask import Flask, request
from flask_pymongo import PyMongo

from config import Config
from mongo_driver import MongoDriver

app = Flask(__name__)
app.config.from_object(Config)
db_driver = MongoDriver(app)

from app import routes
