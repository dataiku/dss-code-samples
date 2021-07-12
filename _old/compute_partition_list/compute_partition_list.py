import dataiku

INPUT_DATASET = "mydataset"
COLUMN_TO_PARTITION_BY = "mypartitioningcolumn"

dataset = dataiku.Dataset(INPUT_DATASET)
df = dataset.get_dataframe(columns = [COLUMN_TO_PARTITION_BY])

combinations = df[COLUMN_TO_PARTITION_BY].unique()
combinations_str = "/".join(combinations)

client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())
variables = project.get_variables()
variables["standard"]["myPartitionList"] = combinations_str
project.set_variables(variables)
