import dataiku
import json

def compare_dataset_schemas(client=None,
                            project_key=None,
                            dataset_a=None,
                            dataset_b=None):
    """Return the common columns (names and types) between two datasets.
    """

    prj = client.get_project(project_key)
    schema_a = prj.get_dataset(dataset_a).get_schema().get("columns")
    schema_b = prj.get_dataset(dataset_b).get_schema().get("columns")
    stringify = lambda s: [json.dumps(x) for x in s]
    dictify = lambda s: [json.loads(x) for x in s]
    common_cols = set(stringify(schema_a)).intersection(stringify(schema_b))
    return common_cols

