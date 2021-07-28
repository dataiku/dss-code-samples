import dataiku

def list_notebooks(client=None):
    """Prints all jupyter notebooks in all projects, distinguishes which notebooks are active as well as the session data for active notebooks
    """ 
    projects = client.list_projects()

    for p in projects :
        proj = client.get_project(p["projectKey"])
        all_notebooks = proj.list_jupyter_notebooks(active=False, as_type="listitems")
        active_notebooks = proj.list_jupyter_notebooks(active=True, as_type="listitems")

        print("\nListing all notebooks for project: " + p["name"])

        for notebook in all_notebooks:   
            print(notebook)

        print("-------------------------------------")
        print("\nACTIVE notebooks for project: " + p["name"])

        for notebook in active_notebooks:
            notebook_object = proj.get_jupyter_notebook(notebook['name']).get_sessions()
            print(notebook)
            print("\n*** Listing session data for notebook: " + notebook['name'] + ' ***')
            print(notebook_object)

        print("-------------------------------------")
