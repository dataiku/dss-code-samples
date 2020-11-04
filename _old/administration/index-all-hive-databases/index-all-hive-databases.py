import dataiku
from dataiku.core.sql import HiveExecutor

he = HiveExecutor(database="default")
client = dataiku.api_client()

databases_list = he.query_to_df("show databases")["database_name"].values
print "Databases: %s" % databases_list

for database in databases_list:
    print "Starting to index %s" % database
    c.catalog_index_connections(["@virtual(hive-jdbc):%s" % database])
    print "Done indexing %s" % database
