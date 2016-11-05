from toolz import assoc
import eventlet
from eventlet.green import urllib2
import xmltodict

feeds = [
    'https://www.google.com/alerts/feeds/09793917664791896102/1298760523418366190',
    'https://www.google.com/alerts/feeds/09793917664791896102/6755748661536211551',
    'https://www.google.com/alerts/feeds/09793917664791896102/9033615043716741803',
    'https://www.google.com/alerts/feeds/09793917664791896102/8709692234058491434',
    'https://www.google.com/alerts/feeds/09793917664791896102/15799638204728333841',
    'https://www.google.com/alerts/feeds/09793917664791896102/13229414712099554011',
    'https://www.google.com/alerts/feeds/09793917664791896102/13229414712099556140'
]

def fetch(url):
    return urllib2.urlopen(url).read()

# fetch raw RSS data via HTTP
def get_entries():

    # create generator from pooled http requests with eventlet
    pool = eventlet.GreenPool(200)
    xml = pool.imap(fetch, feeds)

    # parse xml
    feedlist = (xmltodict.parse(el)['feed'].get('entry') for el in xml)

    # create nested list of entries
    entrylist = (entry if type(entry) == list else [entry] for entry in feedlist if entry)

    # flatten
    return (entry for entries in entrylist for entry in entries)
