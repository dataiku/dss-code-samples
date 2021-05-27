import dataiku

def explore_saved_models(client=None, project_key=None):
    """List saved models of a project and give details on the active versions.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key

    Returns:
        smdl_list: A dict with all saved model ids and perf + algorithm 
                   for the active versions. 

    """
    smdl_list = []
    prj = client.get_project(project_key)
    smdl_ids = [x["id"] for x in prj.list_saved_models()]
    for smdl in smdl_ids:
        data = {}
        obj = prj.get_saved_model(smdl)
        data["version_ids"] = [m["id"] for m in obj.list_versions()]
        active_version_id = obj.get_active_version()["id"]
        active_version_details = obj.get_version_details(active_version_id)
        data["active_version"] = {"id": active_version_id,
                                  "algorithm": active_version_details.details["actualParams"]["resolved"]["algorithm"],
                                  "performance_metrics": active_version_details.get_performance_metrics()}
        smdl_list.append(data)
    return smdl_list


