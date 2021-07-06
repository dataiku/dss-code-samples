import dataikuapi

def delete_deployment(host=None, apiKey=None, deploymentId=None):
    """Delete a deployment on the API Deployer outside DSS
    """ 
    # Instantiate client
    client = dataikuapi.DSSClient(host, apiKey)

    # Retrieve deployment and disable it first
    deployer = client.get_apideployer()
    deployment = deployer.get_deployment(deploymentId)
    settings = deployment.get_settings()
    settings.set_enabled(enabled=True)
    settings.save()

    # Delete deployment once it has been disabled
    update = deployment.start_update()
    update.wait_for_result()
    deployment.delete()