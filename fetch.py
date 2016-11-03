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
    'https://www.google.com/alerts/feeds/09793917664791896102/6755748661536211551',
    'https://www.google.com/alerts/feeds/09793917664791896102/9033615043716741803',
    'https://www.google.com/alerts/feeds/09793917664791896102/8709692234058491434',
    'https://www.google.com/alerts/feeds/09793917664791896102/15799638204728333841',
    'https://www.google.com/alerts/feeds/09793917664791896102/13229414712099554011',
    'https://www.google.com/alerts/feeds/09793917664791896102/13229414712099556140'
]

# fetch raw RSS data via HTTP
data = map(feedparser.parse, feeds)

# collapse into one list and format entries
formatted_data = [ format_entry(entry) for feed in data for entry in feed.entries ]
