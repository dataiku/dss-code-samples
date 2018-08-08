This code sample lists all Hive databases and triggers their indexation, so
that all Hive tables are available through the DSS external tables catalog.

This code sample is designed to run from within DSS, but can be adapted to run outside.

Indexing connections is done in Python through the "catalog_index_connections" method on the "DSSAPIClient" class, which can be obtained using "dataiku.api_client()"
However, this method does not list Hive databases. This in turn can be done using HiveExecutor.

The code sample brings bothh together

