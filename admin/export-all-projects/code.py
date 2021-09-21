import dataiku
import os

def save_instance_projects(client=None, folder_name=None, export_options={}):
    
    current_project = client.get_default_project()
    if not folder_name:
        folder_name = "exports"
        
    if folder_name not in [p["name"] for p in current_project.list_managed_folders()]:
        print("Creating folder {}...".format(folder_name))
        current_project.create_managed_folder(name=folder_name)
        
    folder_path = dataiku.Folder(folder_name).get_path()
    for p in client.list_projects():
        p_key = p["projectKey"]
        # Exclude current project:
        if p_key != current_project.project_key:
            zip_name = p_key + ".zip"
            print("Exporting {}...".format(p_key))
            project = client.get_project(p_key)
            with project.get_export_stream(options=export_options) as s:
                target = os.path.join(folder_path, zip_name)
                if os.path.exists(target):
                    print("SKIPPED (already exists)")
                    continue
                else:
                    with open(target, "wb") as f:
                        for chunk in s.stream(512):
                            f.write(chunk)
                    print("OK")
