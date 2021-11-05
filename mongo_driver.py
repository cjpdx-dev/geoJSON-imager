from flask_pymongo import PyMongo
connection_string = "mongodb+srv://cjpdx:OsY8rrimVnY6vmvB@cluster0.smkta.mongodb.net/db_361?retryWrites=true&w=majority"

class AtlasWriteException(BaseException):
    error_msg = "Database write failed. Make sure you have Atlas admin privileges"

class MongoDriver():

    def __init__(self, app):
        self.driver_client = PyMongo(app, connection_string)
        self.db = self.driver_client.db

    def test_db(self, test_param):
        return self.db.zipcodes.find_one(test_param)

    # def find_zipcode(self, zipcode):

    def populate_db(self):
        file_path = "local_data/US.txt"
        zipcode_collection = self.db.get_collection("zipcodes")

        try:
            with open(file_path, "rt") as raw_file:

                try:
                    for line in raw_file:
                        current_line_data = line.split("\t")
                    
                        collection.insert(
                            {
                                "_id": current_line_data[1],
                                "city": current_line_data[2],
                                "state": current_line_data[4]
                            }
                        )
                except AtlasWriteException():
                    print(e.error_msg)

            raw_file.close()
        
        except FileNotFoundError as e:
            print(e)


if __name__ == "__main__":
    print("Attempted to execute MongoDriver directly.")
else:
    print("Importing MongoDriver")
    