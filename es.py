import dateutil.parser
from toolz import assoc
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
es = Elasticsearch()

def format_entry(entry):
    new_id = 'ge:' + entry['id'][38:]
    return assoc(entry, 'id', new_id)

def create_action(entry):
    return {
        'op_type': 'update',
        '_index': 'alerts-rss',
        '_type': 'alert',
        '_id': entry['id'],
        '_source': entry
    }

def format_reduced(entry):
    return {
        'id': 'ge:' + entry['id'][38:].encode('ascii'),
        'date': dateutil.parser.parse(entry.get('updated')),
        'link': entry['link'].get('@href').encode('ascii'),
        'title':  entry['title'].get('#text').encode('ascii'),
        'body': entry['content'].get('#text').encode('ascii')
    }

def index_to_es(entries):
    formatted_data = (format_entry(entry) for entry in entries)
    actions = (create_action(entry) for entry in formatted_data)
    bulk(es, actions)

def index_reduced(entries):
    formatted_data = (format_reduced(entry) for entry in entries)
    actions = (create_action(entry) for entry in formatted_data)
    bulk(es, actions)
