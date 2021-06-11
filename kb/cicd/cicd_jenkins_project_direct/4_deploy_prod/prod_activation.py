import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]
bundle_file = sys.argv[4] + '.zip'

client = dataikuapi.DSSClient(host, apiKey)
target_project = client.get_project(project)

# Getting the currently active bundle
previous_bundle_id = ""
for project in client.list_projects():
    if project['projectKey'] == project:
        print(project)
        if 'activeBundleState' in project:
            previous_bundle_id = project['activeBundleState']['bundleId']
            break

if not previous_bundle_id:
    print("Cannot find a current active bundle , assuming it is a new project (no rollback possible)")
else:
    print("Currently active bundle id = ", previous_bundle_id)

# Activate the new bundle
latest_bundle = target_project.list_imported_bundles()["bundles"][-1]["bundleId"]
print("Using latest bundle defined as", latest_bundle)
preload_result = target_project.preload_bundle(latest_bundle)
print("Preload result =", preload_result)

try:
    activation_result = target_project.activate_bundle(latest_bundle)
    print("Activation result =", activation_result)
except:
    print("Exception when activating bundle, cancelling operation, previous bundle still active", sys.exc_info()[1])
    sys.exit(1)

# Testing bundle
smoke_test = target_project.get_scenario("TEST_SMOKE")
scenario_result = smoke_test.run_and_wait()

print("*************************")
print("Scenario info: ", scenario_result.get_info())
print("Scenario duration: ", scenario_result.get_duration())
print(scenario_result.get_details()["scenarioRun"]["result"])
print(scenario_result.get_details()["scenarioRun"]["result"]["outcome"])

if scenario_result.get_details()["scenarioRun"]["result"]["outcome"] != "SUCCESS":
    # Rollback
    if not previous_bundle_id:
        print("Error when running smoke test, no rollback possible as this is the first import, please fix manually")
    else:
        target_project.activate_bundle(previous_bundle_id)
        print("Error when running smoke test, bundle has been rollback to the previous version")
    sys.exit(1)
