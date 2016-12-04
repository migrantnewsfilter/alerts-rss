from itertools import islice, takewhile, count
from pymongo import MongoClient, UpdateOne
import dateutil.parser
from datetime import datetime
from bs4 import BeautifulSoup

def clean_html(s):
    return BeautifulSoup(s, 'html5lib').get_text() if s else ''

def prepare_entry(entry):
    return {
        '_id': 'ge:' + entry['id'][38:].encode('ascii'),
        'published': dateutil.parser.parse(entry.get('updated')),
        'added': datetime.utcnow(),
        'content': {
            'link': entry['link'].get('@href').encode('ascii'),
            'title':  clean_html(entry['title'].get('#text')),
            'body': clean_html(entry['content'].get('#text'))
        }
    }

def chunk(n, it):
    src = iter(it)
    return takewhile(bool, (list(islice(src, n)) for _ in count(0)))

def write_entries(client, entries):
    collection = client['newsfilter'].news
    prepared = (prepare_entry(entry) for entry in entries)
    chunked = chunk(20, prepared)

    for c in chunked:
        requests = [ UpdateOne({ '_id': obj['_id']},
                               { '$setOnInsert': obj }
                               , upsert=True) for obj in c]
        collection.bulk_write(requests, ordered=False)
