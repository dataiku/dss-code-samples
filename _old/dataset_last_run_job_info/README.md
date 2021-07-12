# Datasets to Jobs Link

This code sample links the datasets api endpoint to the jobs api endpoint. It leverages
the metrics on a dataset (specifically the computation time of the metrics and the BUILD_START_DATE)
to grab the job that most recently built the dataset from the jobs API.

The goal here was to provide the following three metrics:

* Time dataset started being built - note that this is different from job start time.
* Who built it
* Name of dataset
