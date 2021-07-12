# Compute Partition List

This sample shows how to compute the list of partitions for one given colum in a non-partitioned dataset and store it in a project variable.

This is useful when you start with a raw dataset without partitioning, and use the [Redispath Partitioning](https://www.dataiku.com/learn/guide/other/partitioning/partitioning-redispatch.html) feature of a Sync or Prepare recipe. It will compute the list of partitions required in the "Recipe run options" to build all partitions for further recipes based on the partitioned output.

The list is stored as a project variable in the format expected by Dataiku, i.e. partition1/partition2/etc. You can use it:
- in the Flow by copying and pasting the raw value from the Top bar > ... > Variables,
- in a scenario by referencing the ${myPartitionList} variable.
