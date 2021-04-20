from pymongo import MongoClient, errors, ASCENDING
import urllib

DATABASE_NAME = "RadicaliHomeTest"


class database:

    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.start()

    def start(self):
        # mongo_url = "mongodb://dev_octo:" + urllib.parse.quote("Devel0per)ct0") + "@172.31.18.138/admin"
        mongo_url = "mongodb://localhost:27017/RadicaliHomeTest"
        self.client = MongoClient(mongo_url)
        if self.client is None:
            return "Could not connect to database"
        try:
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[self.collection_name]
        except errors.PyMongoError as e:
            raise e

    def insert(self, data):
        try:
            self.collection.insert_one(data)
            return "Success"
        except errors.PyMongoError as e:
            raise e

    def insert_many(self, data):
        try:
            self.collection.insert_many(data)
            return "Success"
        except errors.PyMongoError as e:
            raise e

    def update(self, query, update):
        try:
            self.collection.update_one(query, update)
            return "Success"
        except errors.PyMongoError as e:
            raise e

    def read(self, query=None):
        result = []
        for x in self.collection.find(query):
            result.append(x)
        return result

    def read_clean(self, query=None):
        result = []
        for x in self.collection.find(query, {'_id': False}):
            result.append(x)
        return result

    def read_clean_20(self, query=None):
        result = []
        for x in self.collection.find(query, {'_id': False}).limit(20):
            result.append(x)
        return result

    def read_clean_sort(self, sort_field, query=None):
        result = []
        for x in self.collection.find(query, {'_id': False}).sort(sort_field, ASCENDING):
            result.append(x)
        return result

    def stop(self):
        self.client.close()

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    COLLECTION_NAME = "inventory_data"
    mongo_db = database_dashboard(COLLECTION_NAME)
    post_data = {
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    }
    import json
    f = open("inventory_data.json")
    data = json.load(f)
    result = mongo_db.insert(data)
    f.close()
    print(result)
