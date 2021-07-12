# this part can be used in a custom scenario's script, or in a "Execute python" step in a step-based scenario
import dataiku
from dataiku.scenario import Scenario

s = Scenario()

dataset_name = 'input_partitioned'
output_name = 'output'
# fetch the partitions
ds = dataiku.Dataset(dataset_name)
all_partitions = ds.list_partitions()
print("Dataset %s has %s partitions" % (dataset_name, len(all_partitions)))

# maybe filter partitions, depending on your usage
partitions_to_build = all_partitions

# build the variable's value as a comma separated string
partition_list_value = ','.join(partitions_to_build)
s.set_scenario_variables(partition_list=partition_list_value)

# in a step-based scenario:
# add a build step to build the output dataset, and set ${partition_list} as the partition identifier

# in a custom scenario:
# launch the build
s.build_dataset(output_name, partitions='${partition_list}')
# alternatively, in a custom scenario, you can pass the value directly, without using a variable
#s.build_dataset(output_name, partitions=partition_list_value)
