This sample shows how to use a variable in a scenario to build a partitioned dataset when the partitions are not all present. 

Normally, when you build a range of partitions for a dataset, say "2018-01-01/2018-01-04", the build fails if one of the dates in the range is missing. The solution is to pass the explicit list of partitions to build, which implies retrieving this list first and passing it as comma-separated.

The flow in the project has input -> input\_partitioned (by date) -> output (partitioned by date). The ouput dataset is build by the scenario on all available partitions.

