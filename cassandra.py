def format_entry(entry):
    return {
        'id': 'ge:' + entry['id'][38:].encode('ascii'),
        'date': d.get('updated').encode('ascii'),
        'link': d['link'].get('@href').encode('ascii'),
        'title': d['title'].get('#text'),
        'body': d['content'].get('#text')
    }

def index_entries(entries):
    formatted_data = (format_entry(entry) for entry in entries)
    # index???
