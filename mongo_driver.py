from flask_pymongo import PyMongo
admin_connection_string = "mongodb+srv://cjpdx:OsY8rrimVnY6vmvB@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"
API_connection_string = "mongodb+srv://API_User:7XgQUH0mL9arQd4p@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"


class AtlasWriteException(Exception):
    error_msg = "Atlas write failed (make sure you are using admin credentials"

class AtlasReadException(Exception):
    error_msg = "Atlas read failed."

class MongoDriver():

    def __init__(self, app):
        # add error handling for bad connection
        self.driver_client = PyMongo(app, API_connection_string)
        self.db = self.driver_client.db

    def test_db(self, test_param):
        return self.db.zipcodes.find_one(test_param)

    def find_zipcode(self, zipcode):
        try:
            query_result = self.db.zipcodes.find_one(zipcode)
            if query_result:
                payload = {"valid_zip": True, "city": query_result["city"], "state": query_result["state"] }
            else:
                payload = {"valid_zip": False, "city": "", "state": "" }
            
            return payload

        except AtlasReadException as e:
            print(e.error_msg)
            return None
            
    def populate_db(self):
        print("For admins only: Do you want to populate the Atlas database? (Y/N): ")
        confirm = input()
        if confirm == "Y" or confirm == "y":
            print("Attempting to populate Atlas database...")
            db_driver.populate_db()
        else:
            print("populate_db aborted")
            return False

        file_path = "local_data/US.txt"
        document_list = []
        zipcode_collection = self.db.get_collection("zipcodes")

        try:
            with open(file_path, "rt") as raw_file:

                for line in raw_file:
                    current_line_data = line.split("\t")
                    document_list.append(
                        {
                            "_id": current_line_data[1],
                            "city": current_line_data[2],
                            "state": current_line_data[4]
                        }
                    )

                try:
                    zipcode_collection.insert_many(document_list)
                
                except AtlasWriteException as e:
                    print(e.error_msg)
                    raise AtlasWriteException
                
                finally:
                    raw_file.close()

            raw_file.close()
        
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError

        print("Finished populating Atlas zipcode collection")
        return True


    