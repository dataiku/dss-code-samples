import dataikuapi
import sys

host = sys.argv[1]
apiKey = sys.argv[2]
project = sys.argv[3]
api_service_id = sys.argv[4]
api_package_id = sys.argv[5]
infra_dev_id = sys.argv[6]
infra_prod_id = sys.argv[7]

client = dataikuapi.DSSClient(host, apiKey)
test_project = client.get_project(project)

####################
# Retrieve the API Service in the project
api_service = test_project.get_api_service(api_service_id)
print("Found API Service to package {}".format(api_service))

####################
# Create and retrieve an API package

api_service.create_package(api_package_id)
print("New package created with name '{}'".format(api_package_id))
# Uncomment the next line to download and use the zip file (to upload it to an Artefact repository for example)
# api_service.download_package_to_file(api_package_id, api_package_id + ".zip")
version_as_stream = api_service.download_package_stream(api_package_id)
print("Stream handle retrieved on the package")

####################
# Find the service as known by API Deployer

api_deployer = client.get_apideployer()
deployer_service = ""
for serv in api_deployer.list_services():
    if serv.id() == api_service_id:
        print("Found existing Deployer API service {}".format(api_service_id))
        deployer_service = serv
if deployer_service == "":
    print("Creating missing service {}".format(api_service_id))
    deployer_service = api_deployer.create_service(api_service_id)

####################
# Import the new version

new_version = deployer_service.import_version(api_package_id, version_as_stream)
print("New version published as '{}'".format(api_package_id))
