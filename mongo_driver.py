from flask_pymongo import PyMongo
admin_connection_string = "mongodb+srv://cjpdx:OsY8rrimVnY6vmvB@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"
API_connection_string = "mongodb+srv://API_User:7XgQUH0mL9arQd4p@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"

class AtlasZipcodeWriteException(Exception):
    msg = "Atlas failed to write zipcode to collection \"zipcodes\" failed. Are you using an admin API key?"

class AtlasZicodeReadException(Exception):
    msg = "Atlas failed to read zipcode from collection \"zipcodes\" "

class AtlasUserWriteException(Exception):
    msg = "Atlas failed to write zipcode to collection \"zipcodes\" "

class AtlasUserReadException(Exception):
    msg = "Atlas failed to read user from collection \"users\" "

class UserEmptyFieldException(Exception):
    msg = "POST user failed. Field was None or empty string"

class UserFieldLengthException(Exception):
    msg = "POST user failed. Field exceeded maximum length."

class MongoDriver():

    def __init__(self, app):
        # TODO: add error handling for bad connection
        # TODO: Look into coding a fix for Melissa's error:
        #       https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3/54511693#54511693
        
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

        except AtlasZipcodeReadException as e:
            print(e.msg)
            return None


    def post_user(self, username, first_name, last_name, zipcode):

        form_fields = [username, first_name, last_name, zipcode]

        for field in form_fields:
            if field is None or field == "":
                print(field + " field was None or empty string. Aborted post_user")
                raise UserEmptyFieldException()

            if len(field) > 50:
                print(field + " field length was larger than 50 characters. Aborted post_user")
                raise UserFieldLengthException() 

        user_document = {
                            "_id": username,
                            "firstName": first_name,
                            "lastName": last_name,
                            "zipCode": zipcode
                        }

        try:
            user_collection = self.db.get_collection("users")
            user_collection.insert_one(user_document) 
        except Exception as e:
            print(e)
            raise AtlasUserWriteException

    def get_user(self, user_id):
        if user_id is None or user_id == "":
                print("user_id was None or empty string. Aborted get_user")
                raise UserEmptyFieldException()
        
        if len(user_id) > 50:
            print("user_id was greater than 50 characters. Aborted get_user")
            raise UserFieldLengthException()

        try:
            query_result = self.db.users.find_one(user_id)

            if query_result:

                payload = { "user_found": True, 
                            "username": query_result["_id"], 
                            "firstName": query_result["firstName"], 
                            "lastName": query_result["lastName"],
                            "zipCode": query_result["zipCode"]
                }

            else:
                payload = { "user_found": False }

            return payload

        except Exception as e:
            print(e)
            raise AtlasUserReadException()


    def update_user(self, user_id, updated_data):
        pass
            

    def populate_db(self):
        
        print("For admins only: Do you want to repopulate the Atlas database? (Y/N): ")
        confirm = input()
        if confirm == "Y" or confirm == "y":
            print("Attempting to populate Atlas database...")
            db_driver.populate_db()
        else:
            print("populate_db aborted")
            return False

        file_path = "local_data/US.txt"

        try:
            with open(file_path, "rt") as raw_file:

                document_list = []
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
                    zipcode_collection = self.db.get_collection("zipcodes")
                    zipcode_collection.insert_many(document_list)
                
                except AtlasZipcodeWriteException as e:
                    print(e.msg)
                    raise AtlasZipcodeWriteException

                finally:
                    raw_file.close()

            raw_file.close()
        
        except FileNotFoundError as e:
            print(e)
            raise FileNotFoundError

        print("Finished populating Atlas zipcode collection")
        return True
