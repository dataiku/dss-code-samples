# this part can be used in a custom scenario's script, or in a "Execute python" step in a step-based scenario
import dataiku
from dataiku.scenario import Scenario

s = Scenario()

#SET DATASET NAMES
# The dataset that gets its partitions added outside of dataiku, or through
# another process should be set in the updated variable
###
# The dataset that the original dataset writes to should be the old variable
updated = 'customers'
old = 'customers_prepared'


# fetch the partitions
def partition_list(dataset):
    return dataiku.Dataset(dataset).list_partitions()

# Get partitions in new set that aren't in old set
partitions_to_build = list(set(partition_list(updated)) - set(partition_list(old)))

# build the variable's value as a comma separated string
partition_list_value = ','.join(partitions_to_build)
s.set_scenario_variables(partition_list=partition_list_value)

print partition_list_value

# in a step-based scenario:
# add a build step to build the output dataset, and set ${partition_list} as the partition identifier

# in a custom scenario:
# alternatively, in a custom scenario, you can pass the value directly, without using a variable
#s.build_dataset(output_name, partitions=partition_list_value)
