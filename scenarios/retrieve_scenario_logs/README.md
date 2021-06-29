# Retrieve scenario logs programatically

## Questions

How can I retrieve the corresponding scenario logs for a scenario found under Last runs > View scenario log in the UI by using Python?

## Answers

TThis is theoretically possible by utilizing the /projects/{projectKey}/scenarios/{scenarioId}/{runId} REST API end-point in addition with the requests package.
