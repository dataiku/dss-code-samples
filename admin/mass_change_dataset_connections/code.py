import dataiku

def mass_change_connection(client=None, project_key=None, origin_conn=None, dest_conn=None):
    """Mass change dataset connections in a project (filesystem connections only)
    """

    prj = client.get_project(project_key)
    all_datasets = prj.list_datasets()
    for d in all_datasets():
        ds = prj.get_dataset(d["name"])
        ds_def = ds.get_definition()
        if ds_def["type"] == "Filesystem":
            if ds_def["params"]["connection"] == origin_conn:
                ds_def["params"]["connection"] == dest_conn
                ds.set_definition(ds_def)
