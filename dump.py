import dateutil.parser
import csv, codecs, cStringIO
import unicodedata

def format_reduced(entry):

    return {
        'id': 'ge:' + entry['id'][38:].encode('ascii'),
        'date': dateutil.parser.parse(entry.get('updated')),
        'link': entry['link'].get('@href').encode('ascii'),
        'title':  unicodedata.normalize('NFKD', entry['title'].get('#text')).encode('ascii','ignore'),
        'summary': unicodedata.normalize('NFKD', entry['content'].get('#text')).encode('ascii','ignore'),
        'label': 'unlabelled',
        'prediction': float(0)
    }

def write_csv(entries, filename = './dump.csv'):
    formatted_data = (format_reduced(entry) for entry in entries)
    keys = ['id', 'date', 'link', 'title', 'summary', 'label', 'prediction']

    with open(filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(formatted_data)

##############################################################
# RUN
#############################################################


from fetch import get_entries
entries = get_entries()
write_csv(entries)
