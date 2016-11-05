import dateutil.parser
from cassandra.cluster import Cluster

cluster = Cluster()

def prepare_entry(entry):
    return {
        'id': 'ge:' + entry['id'][38:].encode('ascii'),
        'date': dateutil.parser.parse(entry.get('updated')),
        'content': {
            'link': entry['link'].get('@href').encode('ascii'),
            'title':  entry['title'].get('#text'),
            'body': entry['content'].get('#text')
        },
        'label': 'unlabelled'
    }

def write_entries(entries):
    session = cluster.connect()

    session.execute("CREATE KEYSPACE IF NOT EXISTS newsfilter WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }"
    )

    session.set_keyspace('newsfilter')

    # prediction could be list??
    session.execute("CREATE TABLE IF NOT EXISTS alerts ( \
    id text, \
    date timestamp, \
    content map<text, text>, \
    label text, \
    prediction float, \
    PRIMARY KEY(id, date) \
    ) WITH CLUSTERING ORDER BY (date DESC)")

    query = "INSERT INTO newsfilter.alerts \
    (id, date, content, label) \
    VALUES (?, ?, ?, ?) IF NOT EXISTS"

    prepared = session.prepare(query)

    prepped_entries = (prepare_entry(entry) for entry in entries)

    # todo batch?
    for e in prepped_entries:
        bound  = prepared.bind(e)
        session.execute(bound)
