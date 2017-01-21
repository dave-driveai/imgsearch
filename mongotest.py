from pymongo import MongoClient
import pprint

client = MongoClient()
db = client['db1']

collection = db['project-GenData']
print(db.collection_names())


# for thing in collection.find({'$and': [{'discrete.color': {"$in": ['red', 'orange']}}, {'discrete.value': {"$in": ['two']}}]}):
#     print(thing)


# for thing in collection.find({'$or': [{'numeric.lol': {'$gt': 20, '$lte': 22}}, {'numeric.lol': {'$gt': 30, '$lte': 31}}]}):
#     print(thing)

for thing in collection.find():
    print(thing)

client.drop_database('db1')