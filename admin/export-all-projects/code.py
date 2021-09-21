import dataiku
import os

from datetime import datetime

def get_current_datetime(fmt="%Y%m%d%H%M%S"):
    now = datetime.now()
    return now.strftime(fmt)


# Create a project where a managed folder will contain all exported projects (except itself)
def get_takeaway_project(client=None, project_key=None):
    """
    Return the handle of a DSSProject where the exports will live.
    If the project doesn't already exist, creates it.
    """
    
    instance_project_keys = client.list_project_keys()
    
    if project_key in instance_project_keys:
        print("Project {} already exists, retrieving handle...".format(project_key))
        project = client.get_project(project_key)
        
    else:
        dt = get_current_datetime()
        if not project_key:
            project_key = "PRJEXPORTS{}".format(dt)
        project_name = "Project exports - {}".format(dt)
        owner = client.get_auth_info()["associatedDSSUser"]
        print("Creating project {} owned by {}...".format(project_key, owner))
        project = client.create_project(project_key=project_key,
                                        name=project_name,
                                        owner=owner)
    return project

    


def export_all_projects(host_project=None, folder_name=None):
    # If folder does not exists, create it
    print("TODO")
    
    # Export all projects and save zip files into managed folder
    print("TODO")
    for p in client.list_projects():
        p_key = p["projectKey"]
        export_name = p_key + ".zip"
        print("Exporting {}...".format(p_key))
        project = client.get_project(p_key)
        with project.get_export_stream() as s:
            target = os.path.join(target_dir, export_name)
            with open(target, "wb+") as f:
                for chunk in s.stream(chunk_size):
                    f.write(chunk)
        print("Export succeded, check output at {}".format(target))
