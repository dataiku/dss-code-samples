import dataiku

def build_all_partitions(scenario=None,
                   project_key=None,
                   input_dataset=None,
                   output_dataset=None):
    """Build all output partitions present in an input dataset.
    Requires input and output datasets to share the same partitioning 
    format.
    Args:
        scenario: A dataiku.scenario.Scenario handle.
        project_key: A string representing the target project key.
        input_dataset: Name of the input dataset from which
                       to list all partitions.
        output_dataset: String of the name of the dataset to build.
    """
    input_dataset = dataiku.Dataset(input_dataset)
    partitions = dataset.list_partitions()
    partitions_str = ','.join(partitions)
    scenario.build_dataset(output_dataset, partitions=partitions_str)

def build_new_partitions(scenario=None,
                   project_key=None,
                   input_dataset=None,
                   output_dataset=None):
    """Build partitions that are present in the input dataset but
    not in the output dataset (= new partitions).
    Requires input and output datasets to share the same partitioning 
    format.
    Args:
        scenario: A dataiku.scenario.Scenario handle.
        project_key: A string representing the target project key.
        input_dataset: Name of the input dataset from which
                       to list all partitions.
        output_dataset: String of the name of the dataset to build.
    """
    input_dataset = dataiku.Dataset(input_dataset)
    output_dataset = dataiku.Dataset(output_dataset)
    input_partitions = set(input_dataset.list_partitions())
    output_partitions = set(output_dataset.list_partitions())
    new_partitions = input_partitions - output_partitions
    partitions_str = ','.join(new_partitions)
    scenario.build_dataset(output_dataset, partitions=partitions_str)




  