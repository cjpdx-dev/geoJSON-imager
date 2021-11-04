from config import Config
from flask_pymongo import PyMongo
import os

def create_zipcodes_db(db_client: PyMongo()):

    collection = db_client.db.get_collection("zipcodes")
    file_path = "data/US.txt"

    with open(file_path, "rt") as raw_file:

        for line in raw_file:
            current_line_data = line.split("\t")
            collection.insert(
                { 
                "_id": current_line_data[1], 
                "city": current_line_data[2],
                "state": current_line_data[4]
                }
            )


        raw_file.close()
        print("zipcodes collection created")
    
    return

if __name__ == "__main__":
    print("Attempted to execute db_scripts directly.")
else:
    print("Importing db_scripts.py")
    
