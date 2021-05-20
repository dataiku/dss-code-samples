import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
api_service_id = sys.argv[4]
api_package_id = sys.argv[5]
infra_prod_id = sys.argv[6]

client = dataikuapi.DSSClient(host, apiKey)

####################
# Retrieve the service object from API Deployer
api_deployer = client.get_apideployer()
deployer_service = ""
for serv in api_deployer.list_services():
    if serv.id() == api_service_id:
        print("Found existing Deployer API service (" + api_service_id + ")")
        deployer_service = serv

if deployer_service == "":
    print("Cannot find the required API service named '{}'".format(api_service_id))
    sys.exit(1)

####################
# Find if there is an existing deployment to update or a new to create

print("Looking for existing deployments of '" + deployer_service.id() + "' on infrastructure '" + infra_prod_id + "'")
serv_status = deployer_service.get_status()
dep_to_update = ""
running_version = ""
for dep in serv_status.get_raw()['deployments']:
    if infra_prod_id == dep['infraId']:
        print("Found deployment to update -> " + dep['id'])
        dep_to_update = api_deployer.get_deployment(dep['id'])

if dep_to_update == "":
    # CREATE A DEPLOYMENT
    print("CREATING DEPLOYMENT")
    dep_id = deployer_service.id() + "-on-" + infra_prod_id
    dep_to_update = api_deployer.create_deployment(dep_id, deployer_service.id(), infra_prod_id, api_package_id)
else:
    # UPDATE DEPLOYMENT
    print("UPDATING DEPLOYMENT")
    print("Current deployment '{}' on infra '{}' with API package '{}' is in status '{}'".format(
        dep_to_update.get_settings().get_raw()['id'],
        dep_to_update.get_settings().get_raw()['infraId'],
        dep_to_update.get_settings().get_raw()['generationsMapping']['generation'],
        dep_to_update.get_status().get_health()
    ))
    running_version = dep_to_update.get_settings().get_raw()['generationsMapping']['generation']
    settings_to_deploy = dep_to_update.get_settings()
    settings_to_deploy.set_single_version(api_package_id)
    settings_to_deploy.save()

####################
# Request API Deployer to update the API node

update_exec = dep_to_update.start_update()
print("Update launched -> {}".format(update_exec.get_state()))
update_exec.wait_for_result()
print("  --> Update done with result => " + str(update_exec.get_result()))

print("New deployment '{}' on infra '{}' with API version '{}' is in status '{}'".format(
    dep_to_update.get_settings().get_raw()['id'],
    dep_to_update.get_settings().get_raw()['infraId'],
    dep_to_update.get_settings().get_raw()['generationsMapping']['generation'],
    dep_to_update.get_status().get_health()
))

####################
# Test and rollback if needed

if dep_to_update.get_status().get_health() != 'HEALTHY':
    if running_version == "":
        print("Deployment failed, cannot roll back, aborting")
        sys.exit(1)
    else:
        print("Deployment failed, rolling back to previously running API package {}".format(running_version))
        rollback_settings = dep_to_update.get_settings()
        rollback_settings.set_single_version(running_version)
        rollback_settings.save()
        update_exec = dep_to_update.start_update()
        print("Rollback launched -> {}".format(update_exec.get_state()))
        update_exec.wait_for_result()
        print("  --> Rollback done with result => " + str(update_exec.get_result()))
        if dep_to_update.get_status().get_health() == 'HEALTHY':
            print("Rollback successful")
            sys.exit(2)
        else:
            print("Rollback failed")
            sys.exit(1)

print('Deployment successful')
