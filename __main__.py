from lib.mongo import write_entries
from lib.fetch import get_entries
from lib.feeds import get_feeds
from pymongo import MongoClient
import os
import schedule
import time

########################################################
# Load into Mongo
########################################################

def write_to_mongo():
    client = MongoClient(
        host = os.environ.get('MONGO_HOST') or None
    )
    feeds = get_feeds(client)
    entries = get_entries(feeds)
    write_entries(client, entries)
    client.close()


if __name__ == '__main__':

    # write once on startup
    write_to_mongo()

    # schedule to run again
    schedule.every(5).minutes.do(write_to_mongo)

    # run the scheduler!
    while True:
        schedule.run_pending()
        time.sleep(10)
