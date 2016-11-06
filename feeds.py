from pymongo import MongoClient

def get_feeds(client):
    collection = client['newsfilter'].feeds
    feeds =  collection.find_one({ '_id': 'feeds' })
    return feeds['feeds']
