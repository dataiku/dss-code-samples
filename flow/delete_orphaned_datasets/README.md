# Delete orphaned datasets

## Questions
* I want to programmatically remove from my flow any dataset that is not linked to any recipe.

## Answers
This is possible by using the [Flow API](https://doc.dataiku.com/dss/latest/python-api/flow.html) and listing nodes that have no predecessors and successors in the Flow graph.
