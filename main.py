import json
import re
import requests
from pymongo import MongoClient, ASCENDING, DESCENDING
from flask import Flask, render_template, request, abort, send_from_directory
from bson import json_util
from params import *

app = Flask(__name__)

NUM_RANGE_PATTERN = re.compile('(\[|\()(\d+)\s*,\s*(\d+)(\]|\))')

projects = {}
volume_lookup = {}


def get_image_url(img_id):
    volume = img_id.split(",")[0]
    if volume not in volume_lookup:
        getresult = requests.get(SEAWEED_LOOKUP_URL + str(volume))
        location_data = json.loads(getresult.content.decode("utf-8"))
        port = location_data["locations"][0]["url"].split(":")[1]
        volume_lookup[volume] = port
    return HOST_IP + ":" + str(volume_lookup[volume]) + "/" + img_id


class Mongo:

    def __init__(self):
        self.db = MongoClient()[DB]
        self.pcol = self.db[PROJECT_COLLECTION]
        for data in self.pcol.find():
            projects[data[PROJECT_NAME_KEY]] = Project(data)

    def add_project(self, data):
        self.pcol.insert_one(data)

    def delete_project(self, project):
        collection = self.db[ITEM_COLLECTION_PREFIX + project]
        for item in collection.find():
            requests.delete(get_image_url(item[ITEM_IMAGE_KEY]))
        collection.drop()
        self.pcol.delete_one({PROJECT_NAME_KEY: project})
        del projects[project]

    def get_items(self, project, query=None):
        return self.db[ITEM_COLLECTION_PREFIX + project].find(query)

    def get_projects_names(self):
        cursor = self.pcol.find()
        names = []
        for project in cursor:
            names.append(project[PROJECT_NAME_KEY])
        return names

    def get_size(self, project):
        return self.db[ITEM_COLLECTION_PREFIX + project].find().count()


class Project:

    def __init__(self, data):
        self.name = data[PROJECT_NAME_KEY]
        self.id_fields = data[PROJECT_ID_KEY]
        self.numeric_fields = data[PROJECT_NUMERIC_KEY]
        self.discrete_fields = data[PROJECT_DISCRETE_KEY]


def get_project(project_name):
    if project_name not in projects.keys():
        abort(404)
    return projects[project_name]


# API stuff

@app.route("/api/newProject", methods=['POST'])
def new_project():
    data = json.loads(request.form['json'])
    if data[PROJECT_NAME_KEY] in projects.keys():
        return "project already exist"
    project = Project(data)
    projects[data[PROJECT_NAME_KEY]] = project
    mongo.add_project(data)
    return "project created"


@app.route("/api/delete/<name>", methods=['POST'])
def delete_project(name):
    mongo.delete_project(name)
    return "project deleted"


def to_filter(arg, value):
    values = value.split()
    field = arg[1:]
    if arg[0] == 'n':
        nfilters = []
        for val in values:
            m = NUM_RANGE_PATTERN.match(val)
            if not m:
                continue
            gt = "$gt" if m.group(1) == '(' else "$gte"
            lt = "$lt" if m.group(4) == ')' else "$lte"
            nfilters.append({ITEM_NUMERIC_PREFIX + "." + field: {gt: int(m.group(2)), lt: int(m.group(3))}})
        return {"$or": nfilters}
    elif arg[0] == 'd':
        return {ITEM_DISCRETE_PREFIX + "." + field: {"$in": values}}


@app.route("/api/query/<name>")
def query_project(name):
    filters = []
    amount = 50
    offset = 0
    sort_field = "_id"
    sort_order = ASCENDING
    for arg in request.args:
        value = request.args.get(arg)
        if not value:
            continue
        if arg == "amount":
            amount = int(value)
        elif arg == "offset":
            offset = int(value)
        elif arg == "sortField":
            if value[0] == 'n':
                sort_field = ITEM_NUMERIC_PREFIX + "." + value[1:]
            else:
                sort_field = value
        elif arg == "sortOrder":
            order_val = int(value)
            if order_val == ASCENDING or order_val == DESCENDING:
                sort_order = order_val
        elif arg[0] == 'n' or arg[0] == 'd':
            filters.append(to_filter(arg, value))

    query = {} if not filters else {"$and": filters}
    cursor = mongo.get_items(name, query)
    total = cursor.count()
    cursor.skip(offset).limit(amount).sort(sort_field, sort_order)
    results = []
    for result in cursor:
        result[ITEM_IMAGE_KEY] = get_image_url(result[ITEM_IMAGE_KEY])
        results.append(result)
    return json_util.dumps({"results": results, "total": total, "amount": amount, "offset": offset})


# pages

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html', projects=mongo.get_projects_names())


@app.route("/status", methods=['GET'])
def status_page():
    projs = {}
    for name in mongo.get_projects_names():
        projs[name] = mongo.get_size(name)
    return render_template('status.html', projects=projs)


@app.route("/search/<name>")
def search_page(name):
    project = get_project(name)
    return render_template('search.html', project=project)


mongo = Mongo()
app.run(host='0.0.0.0', threaded=True)
