from pymongo import MongoClient

def get_feeds(client):
    collection = client['newsfilter'].terms
    feeds =  collection.find_one({ '_id': 'alerts' })
    return feeds.get('feeds')
