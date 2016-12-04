from toolz import assoc
import eventlet
from eventlet.green import urllib2

import xmltodict

def fetch(url):
    return urllib2.urlopen(url).read()

# fetch raw RSS data via HTTP
def get_entries(feeds):

    # create generator from pooled http requests with eventlet
    pool = eventlet.GreenPool(200)
    xml = pool.imap(fetch, feeds)

    # parse xml
    feedlist = (xmltodict.parse(el)['feed'].get('entry') for el in xml)

    # create nested list of entries
    entrylist = (entry if type(entry) == list else [entry] for entry in feedlist if entry)

    # flatten
    return (entry for entries in entrylist for entry in entries)
