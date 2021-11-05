import dataikuapi
import pprint

from typing import Dict

def get_instance_notebooks(client: dataikuapi.dssclient.DSSClient) -> Dict:
    all_notebooks = dict()
    for p in client.list_projects():
        p_key = p["projectKey"]
        project = client.get_project(p_key)
        project_notebooks = project.list_jupyter_notebooks()
        if project_notebooks:
            notebooks = []
            for nb in project_notebooks:
                # If the notebook is active then it has at least 1 running session
                sessions = nb.get_sessions()
                if sessions:
                    status = "ACTIVE - {} session(s)".format(len(sessions))
                else:
                    status = "INACTIVE"
                notebooks.append({"name": nb.notebook_name,
                                  "status": status})
            all_notebooks[p_key] = notebooks
    return all_notebooks

def pprint_instance_notebooks(client: dataikuapi.dssclient.DSSClient):
    all_notebooks = get_instance_notebooks(client)
    pprint.pprint(all_notebooks)
    
