from itertools import islice, takewhile, count
from pymongo import MongoClient, UpdateOne
import dateutil.parser
from datetime import datetime

client = MongoClient()

def prepare_entry(entry):
    return {
        '_id': 'ge:' + entry['id'][38:].encode('ascii'),
        'published': dateutil.parser.parse(entry.get('updated')),
        'added': datetime.now(),
        'content': {
            'link': entry['link'].get('@href').encode('ascii'),
            'title':  entry['title'].get('#text'),
            'body': entry['content'].get('#text')
        }
    }

def chunk(n, it):
    src = iter(it)
    return takewhile(bool, (list(islice(src, n)) for _ in count(0)))

def write_entries(entries):
    collection = client['newsfilter'].alerts

    prepared = (prepare_entry(entry) for entry in entries)
    chunked = chunk(10, prepared)

    # unordered should ignore errors - is this performant??
    for e in chunked:
        collection.insert_many(e, ordered=False)
