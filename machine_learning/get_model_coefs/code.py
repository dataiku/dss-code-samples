def get_model_coefficients(client, project_key=None, model_id=None, version_id=None):
    """
    This function returns a dictionary with the coefficient names and values from a
    given DSS model and version in a project.
    :param object client: A DSS client handle
    :param str project_key: The key of the project where the model resides
    :param str model_id: The model id
    :param str version_id: The version of the model. Defaults to the active model
            if no version id is specified.
    :return: A dictionary with key="coefficient name" and value=coefficient
    """

    project = client.get_project(project_key)
    model = project.get_saved_model(model_id)
    if version_id is None:
        version_id = model.get_active_version().get('id')
    details = model.get_version_details(version_id)
    details_lr = details.details.get('iperf', {}).get('lmCoefficients', {})
    rescaled_coefs = details_lr.get('rescaledCoefs', [])
    variables = details_lr.get('variables',[])
    coef_dict = {var: coef for var, coef in zip(variables, rescaled_coefs)}
    if len(coef_dict)==0:
        print(f"Model {model_id} and version {version_id} does not have coefficients")
    return coef_dict
