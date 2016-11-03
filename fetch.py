import feedparser
from toolz import assoc



##################################################
# Functions
#################################################

def format_entry(entry):
    new_id = entry['id'][38:] # encode ascii
    return assoc(entry, 'id', new_id)





####################################################
# Run
####################################################

feeds = [
    'https://www.google.com/alerts/feeds/09793917664791896102/1298760523418366190',
    'https://www.google.com/alerts/feeds/09793917664791896102/9033615043716741803'
]

# fetch raw RSS data via HTTP
data = map(feedparser.parse, feeds)

# collapse into one list and format entries
formatted_data = [ format_entry(entry) for feed in data for entry in feed.entries ]
