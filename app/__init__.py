
from flask import Flask, request
from flask_pymongo import PyMongo

from config import Config
from mongo_driver import MongoDriver
connection_string = "mongodb+srv://cjpdx:OsY8rrimVnY6vmvB@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"


app = Flask(__name__)
app.config.from_object(Config)

db_driver = MongoDriver(app)
test_param = {"hello" : "world"}
query_result = db_driver.test_db(test_param)

# Uncomment to popuate atlas db (yeah...there has to be a better way than this..)
print("For admins only: Do you want to populate the Atlas database? (Y/N): ")
confirm = input()
if confirm == "Y" or confirm == "y":
    print("Attempting to populate Atlas database...")
    db_driver.populate_db()
else:
    print("Skipped")

# mongo_client = PyMongo(app, connection_string)
# db = mongo_client.db
# query_result = db.zipcodes.find_one({"hello": "world"})
# zipcode_collection = db.get_collection("zipcodes")
# query_result = zipcode_collection.find_one({"hello": "world"})
print(query_result)

from app import routes
