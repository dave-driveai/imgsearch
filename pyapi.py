import requests
import json
from pymongo import MongoClient
from params import *
import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class Project:

    def __init__(self, name, ids, numeric, discrete, db):
        self.name = name
        self.id_fields = ids
        self.numeric_fields = numeric
        self.discrete_fields = discrete
        self.db_collection = db[ITEM_COLLECTION_PREFIX + name]

    def __add_data(self, image, meta_data, session=None):
        if isinstance(image, str):
            image = open(image, 'rb')
        result = requests.post(SEAWEED_ASSIGN_URL)
        image_db_data = json.loads(result.content.decode("utf-8"))
        if SEAWEED_FID not in image_db_data:
            print("NO SEAWEED D:")
            return
        port = image_db_data['url'].split(":")[1]
        image_db_path = HOST_IP + ":" + str(port) + "/" + image_db_data[SEAWEED_FID]
        if session:
            print("session put")
            result = session.put(image_db_path, files={'file': image}, stream=False)
            print(result.content)
        else:
            print("WTF")
            requests.post(image_db_path, files={'file': image})
        meta_data[ITEM_IMAGE_KEY] = image_db_data[SEAWEED_FID]
        self.db_collection.insert_one(meta_data)

    def add_data(self, image, ids, numeric_meta, discrete_meta, session=None):
        meta_data = {ITEM_ID_PREFIX: ids, ITEM_NUMERIC_PREFIX: numeric_meta, ITEM_DISCRETE_PREFIX: discrete_meta}
        self.__add_data(image, meta_data, session)

    def add_fdata(self, image, meta_file, session=None):
        meta_data = json.loads(open(meta_file, 'r').read())
        self.__add_data(image, meta_data, session)


class Client:
    def __init__(self):
        self.db = MongoClient()[DB]

    def __create_project(self, data):
        requests.post(SERVER_URL + "/api/newProject", {'json': json.dumps(data)})
        return Project(data[PROJECT_NAME_KEY], data[PROJECT_ID_KEY], data[PROJECT_NUMERIC_KEY],
                       data[PROJECT_DISCRETE_KEY], self.db)

    def create_project(self, name, id_fields, numeric_fields, discrete_fields, image_db=None):
        data = {PROJECT_NAME_KEY: name, PROJECT_ID_KEY: id_fields, PROJECT_NUMERIC_KEY: numeric_fields,
                PROJECT_DISCRETE_KEY: discrete_fields}
        return self.__create_project(data)

    def create_fproject(self, meta_file):
        data = json.loads(open(meta_file, 'r').read())
        return self.__create_project(data)
