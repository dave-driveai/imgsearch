import json
import re
from pymongo import MongoClient
from flask import Flask, render_template, request, abort, send_from_directory

app = Flask(__name__)

DB = "db1"
PROJECT_COLLECTION = "projects"
COLLECTION_PREFIX = "project-"
DB_ID_PREFIX = "id"
DB_NUMERIC_PREFIX = "numeric"
DB_DISCRETE_PREFIX = "discrete"

# TODO for development
HOST_IP = "http://edamame2"

SEAWEED_VOLUME_URL = HOST_IP + ":8080/"

NUM_RANGE_PATTERN = re.compile('(\[|\()(\d+)\s*,\s*(\d+)(\]|\))')

projects = {}


class Mongo:

    def __init__(self):
        self.db = MongoClient()[DB]
        self.pcol = self.db[PROJECT_COLLECTION]
        for data in self.pcol.find():
            projects[data['name']] = Project(data['name'], data['idf'], data['numericf'], data['discretef'])

    def add_project(self, data):
        self.pcol.insert_one(data)

    def get_items(self, project, query=None):
        return self.db[COLLECTION_PREFIX + project].find(query)


class Project:

    def __init__(self, name, ids, numeric, discrete):
        self.name = name
        self.id_fields = ids
        self.numeric_fields = numeric
        self.discrete_fields = discrete


def get_project(project_name):
    if project_name not in projects.keys():
        abort(404)
    return projects[project_name]


# API stuff

@app.route("/api/testPost", methods=['POST'])
def testp():
    try:
        f = request.files['file']
        f.save('var/uploads/FLSKSEVERAAA.txt')
    except KeyError:
        print("key error")
    print(request.form['type'])
    return "test response"


@app.route("/api/newProject", methods=['POST'])
def new_project():
    data = json.loads(request.form['json'])
    if data['name'] in projects.keys():
        return "project already exist"
    proj = Project(data['name'], data['idf'], data['numericf'], data['discretef'])
    projects[data['name']] = proj
    mongo.add_project(data)
    return "project created"


@app.route("/api/projects", methods=['GET'])
def get_projects():
    return json.dumps(list(projects.keys()))


@app.route("/api/projectmeta/<name>")
def get_project_meta(name):
    project = get_project(name)
    return json.dumps({'id': project.id_fields, 'numeric': project.numeric_fields, 'discrete': project.discrete_fields})


@app.route("/api/projectdata/<name>")
def get_project_data(name):
    ret = ""
    for item in mongo.get_items(name):
        ret += str(item) + "<br/>"
    return ret


# pages

@app.route("/", methods=['GET'])
def home_page():
    return render_template('index.html', projects=projects)


@app.route("/results/<name>")
def result_page(name):
    filters = []
    result_per_page = 50
    page = 1
    for arg in request.args:
        value = request.args.get(arg)
        if not value:
            continue
        if arg == "resultsper":
            result_per_page = int(value)
            continue
        elif arg == "page":
            page = int(value)
        vals = value.split()
        field = arg[1:]
        if arg[0] == 'n':
            nfilters = []
            for val in vals:
                m = NUM_RANGE_PATTERN.match(val)
                if not m:
                    continue
                gt = "$gt" if m.group(1) == '(' else "$gte"
                lt = "$lt" if m.group(4) == ')' else "$lte"
                nfilters.append({DB_NUMERIC_PREFIX + '.' + field: {gt: int(m.group(2)), lt: int(m.group(3))}})
            filters.append({"$or": nfilters})
        elif arg[0] == 'd':
            filters.append({DB_DISCRETE_PREFIX + '.' + field: {"$in": vals}})

    query = {} if not filters else {"$and": filters}
    print(query)
    cursor = mongo.get_items(name, query)
    total = cursor.count()
    page = max(1, min(page, (total-1)//result_per_page+1))
    cursor.skip((page-1)*result_per_page).limit(result_per_page)
    results = []
    for result in cursor:
        result['img'] = SEAWEED_VOLUME_URL + result['img']
        results.append(result)
    return render_template('results.html', results=results, total=total, perpage=result_per_page, pageNo=page)


@app.route("/search/<name>")
def search_page(name):
    project = get_project(name)
    return render_template('search.html', project=project)


mongo = Mongo()
app.run(host='0.0.0.0', threaded=True)
