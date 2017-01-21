import requests
import json
from pymongo import MongoClient

DB = "db1"
COLLECTION_PREFIX = "project-"
DB_ID_PREFIX = "id"
DB_NUMERIC_PREFIX = "numeric"
DB_DISCRETE_PREFIX = "discrete"

# TODO for development
HOST_IP = "http://edamame2"

SERVER_URL = HOST_IP + ":5000"
SEAWEED_ASSIGN_URL = HOST_IP + ":9333/dir/assign"
SEAWEED_VOLUME_URL = HOST_IP + ":8080/"


def post_request(url, data):
    return requests.post(SERVER_URL + url, {'json': data})


class Project:

    def __init__(self, name, ids, numeric, discrete, db):
        self.name = name
        self.id_fields = ids
        self.numeric_fields = numeric
        self.discrete_fields = discrete
        self.dbcollection = db[COLLECTION_PREFIX + name]

    def __add_data(self, image, meta_data):
        if isinstance(image, str):
            image = open(image, 'rb')
        result = requests.post(SEAWEED_ASSIGN_URL)
        image_db_data = json.loads(result.content.decode("utf-8"))
        if 'fid' not in image_db_data:
            print("NO SEAWEED D:")
            return
        image_db_path = SEAWEED_VOLUME_URL + image_db_data['fid']
        result = requests.post(image_db_path, files={'file': image})
        print(result.content)
        meta_data['img'] = image_db_data['fid']
        self.dbcollection.insert_one(meta_data)

    def add_data(self, image, ids, numeric_meta, discrete_meta):
        meta_data = {'project': self.name, DB_ID_PREFIX: ids, DB_NUMERIC_PREFIX: numeric_meta,
                     DB_DISCRETE_PREFIX: discrete_meta}
        self.__add_data(image, meta_data)

    def add_fdata(self, image, meta_file):
        meta_data = json.loads(open(meta_file, 'r').read())
        self.__add_data(image, meta_data)


class Client:

    def __init__(self):
        self.db = MongoClient()[DB]

    def __create_project(self, data):
        post_request("/api/newProject", json.dumps(data))
        return Project(data['name'], data['idf'], data['numericf'], data['discretef'], self.db)

    def create_project(self, name, id_fields, numeric_fields, discrete_fields, image_db=None):
        data = {'name': name, 'idf': id_fields, 'numericf': numeric_fields, 'discretef': discrete_fields}
        return self.__create_project(data)

    def create_fproject(self, meta_file):
        data = json.loads(open(meta_file, 'r').read())
        return self.__create_project(data)

# requests.post("http://127.0.0.1:5000/api/newProject", {"json":json.dumps({'name':'p1'})})
