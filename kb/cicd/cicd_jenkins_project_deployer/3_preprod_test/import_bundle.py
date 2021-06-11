import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]
bundle_id = sys.argv[4]
infra = sys.argv[5]

client = dataikuapi.DSSClient(host,apiKey )
pdpl = client.get_projectdeployer()

# Create or update a deployment
print("Searching for existing deployment of '{}' on infra '{}'".format( project , infra))
pdpl_proj = pdpl.get_project(project)
deployments = pdpl_proj.get_status().get_deployments(infra)

if deployments :
    #update
    deployment = deployments[0]
    print("Using existing deployment '{}'".format(deployment.id))
    depl_settings = deployment.get_settings()
    depl_settings.get_raw()['bundleId'] = bundle_id
    depl_settings.save()
else :
    #create
    print("Need to create a new deployment")
    dp_id = pdpl_proj.id + '-on-' + infra
    deployment = pdpl.create_deployment(dp_id, pdpl_proj.id, infra, bundle_id)
    print("New deployment created as {}".format(deployment.id))

print("Deployment ready to update => {}".format(deployment.id))

# Update the automation node

update_exec = deployment.start_update()
print("Update launched -> {}".format(update_exec.get_state()))
update_exec.wait_for_result()
print("  --> Update done with result => " + str(update_exec.get_result()))

print("Deployment done '{}' on infra '{}' with bundle ID '{}' => status '{}'".format(
    deployment.id,
    deployment.get_settings().get_raw()['infraId'],
    deployment.get_settings().get_raw()['bundleId'],
    deployment.get_status().get_health()
))

if deployment.get_status().get_health() == "ERROR" :
    print("Error when deploying the model to preprod, aborting")
    print(deployment.get_status().get_health_messages())
    sys.exit(1)
