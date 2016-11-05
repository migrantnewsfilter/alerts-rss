from es import index_to_es, index_reduced
from cass import write_entries

from fetch import get_entries


entries = get_entries()




########################################################
# Cassandra
########################################################
write_entries(entries)



########################################################
# ES
########################################################

index_to_es(entries)
