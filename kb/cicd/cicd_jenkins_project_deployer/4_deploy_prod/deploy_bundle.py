import dataikuapi
import sys

pdpl_host = sys.argv[1]
pdpl_apiKey = sys.argv[2]
project = sys.argv[3]
bundle_id = sys.argv[4]
infra = sys.argv[5]
auto_host = sys.argv[6]
auto_apiKey = sys.argv[7]

previous_bundle_id = ""
failed_deployment = False

# Deploy the new bundle
print("Searching for existing deployment of '{}' on infra '{}'".format( project , infra))
pdpl_client = dataikuapi.DSSClient(pdpl_host, pdpl_apiKey)
pdpl = pdpl_client.get_projectdeployer()
pdpl_proj = pdpl.get_project(project)
deployments = pdpl_proj.get_status().get_deployments(infra)

if deployments :
    #update
    deployment = deployments[0]
    print("Using existing deployment '{}'".format(deployment.id))
    depl_settings = deployment.get_settings()
    previous_bundle_id = depl_settings.get_raw()['bundleId']
    depl_settings.get_raw()['bundleId'] = bundle_id
    depl_settings.save()
else :
    #create
    print("Need to create a new deployment (no rollback possible)")
    dp_id = pdpl_proj.id + '-on-' + infra
    deployment = pdpl.create_deployment(dp_id, pdpl_proj.id, infra, bundle_id)
    print("New deployment created as {}".format(deployment.id))

print("Deployment ready to update => {}".format(deployment.id))
update_exec = deployment.start_update()
print("Update launched -> {}".format(update_exec.get_state()))
update_exec.wait_for_result()

if deployment.get_status().get_health() == "ERROR" :
    print("Error when deploying the model to production, need to rollback: {}".format(deployment.get_status().get_health_messages()))
    failed_deployment = True
else :
    print("Deployment successful")    

# Smoke test and rollback
if not failed_deployment :
    auto_client = dataikuapi.DSSClient(auto_host, auto_apiKey)
    target_project = auto_client.get_project(project)
    smoke_test = target_project.get_scenario("TEST_SMOKE")
    scenario_result = smoke_test.run_and_wait()

    print("*************************")
    print("Scenario info: ", scenario_result.get_info())
    print("Scenario duration: ", scenario_result.get_duration())
    print(scenario_result.get_details()["scenarioRun"]["result"])
    print(scenario_result.get_details()["scenarioRun"]["result"]["outcome"])
    if scenario_result.get_details()["scenarioRun"]["result"]["outcome"] != "SUCCESS":
        print("Error when running smoke test, need to rollback")
        failed_deployment = True

if failed_deployment :
    print("Starting rollback process")
    # Rollback
    if not previous_bundle_id:
        print("No rollback possible, please fix manually")
    else:
        depl_settings = deployment.get_settings()
        depl_settings.get_raw()['bundleId'] = previous_bundle_id
        depl_settings.save()
        update_exec = deployment.start_update()
        print("Update launched -> {}".format(update_exec.get_state()))
        update_exec.wait_for_result()
        print("  --> Update done with result => " + str(update_exec.get_result()))

        print("Rollback done '{}' on infra '{}' to bundle ID '{}' => status '{}'".format(
            deployment.id,
            deployment.get_settings().get_raw()['infraId'],
            deployment.get_settings().get_raw()['bundleId'],
            deployment.get_status().get_health()
        ))
    sys.exit(1)
