import dataiku

def delete_deployment(deploymentId=None):
    """Delete a deployment on the API Deployer inside DSS
    """ 
    # Instantiate client
    client = dataiku.api_client()
    
    # Retrieve deployment and disable it first
    deployer = client.get_apideployer()
    deployment = deployer.get_deployment(deploymentId)
    settings = deployment.get_settings()
    settings.set_enabled(enabled=False)
    settings.save()

    # Delete deployment once it has been disabled
    update = deployment.start_update()
    update.wait_for_result()
    deployment.delete()
