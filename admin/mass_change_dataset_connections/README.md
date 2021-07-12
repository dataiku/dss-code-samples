# Mass-change dataset connections 

## Questions
* In a project, I want to programmatically switch all datasets from a given connection to a different connection, thus reproducing the "Change connection" action available in the DSS visual UI. 

## Answers
This is possible with the `get_definition()` and `set_definition()` methods related to [datasets](https://doc.dataiku.com/dss/latest/python-api/datasets-reference.html) in the DSS public API.

## Warnings
* Once the connection change is done, you will need to rebuild all modified datasets.
* This example only works for filesystem connections.
