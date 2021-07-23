# Retrieve scenario logs programatically

## Questions

How can I retrieve the corresponding scenario logs for a scenario found under Last runs > View scenario log in the UI by using Python?

## Answers

This is theoretically possible by utilizing the /projects/{projectKey}/scenarios/{scenarioId}/{runId} REST API end-point in addition with the requests package.
Similar to what DSSScenarioRun.get_info() provides, but some more added information such as what permissions the "run as user" has when running the scenario.
