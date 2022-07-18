import dataiku 
from dataiku import SQLExecutor2

# Create a mapping between instance types and corresponding connection names.
conn_mapping = {"DESIGN": "my_design_connection",
                "AUTOMATION": "my_prod_connection"}

# Retrieve the current Dataiku instance type
client = dataiku.api_client()
instance_type = client.get_instance_info().node_type

# Instanciate a SQLExecutor2 object with the appropriate connection
executor = SQLExecutor2(connection=conn_mapping[instance_type])
