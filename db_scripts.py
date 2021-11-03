from config import Config
from flask_pymongo import PyMongo

import os

# def test_script(db_client: PyMongo()):
#     print('hello world, this is test_script')
#     print(db_client.db.last_status())
#     print(db_client.db.name)

def repopulate_db(db_client: PyMongo()):

    # print("Warning: executing this script will repopulate db.zipcodes - Are you sure you want to proceed? (Y/N): ")
    # user_input = input()
    # if user_input != 'Y' and user_input != 'y':    
    #     print("Aborting populate_db_zipcodes()")
    # return 0

    db_client.db.drop_collection("zipcodes")

    file_path = "data/US.txt"

    with open(file_path, "rt") as raw_file:
        print(raw_file.readline())

        max_lines = 10
        for line in raw_file:
            current_line_data = line.split("\t")
            print("Zipcode: ", current_line_data[1], " City: ", current_line_data[2], " State: ", current_line_data[4])
            
        raw_file.close()
        

if __name__ == "__main__":
    print("Attempted to execute db_scripts directly.")
else:
    print("Importing db_scripts.py")
