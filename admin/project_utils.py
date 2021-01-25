import dataiku

def edit_project_permissions(client=None, project_key=None, group=None, perms=None, revoke=False):
    """Grant or revoke project permissions for a given group.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key
        group: A string representing the target group name
        perms: A list of permissions to grant 
        revoke: A boolean for completely revoking access to the project
    """

    prj = client.get_project(project_key)
    perm_obj = prj.get_permissions()
    perm_list = perm_obj["permissions"]
    for p in perm_list:
        if p["group"] == group:
            print("Deleting existing permissions...")
            perm_list.remove(p)
    if revoke:
        perm_obj["permissions"] = perm_list
        print(f"Revoking all permissions on project {project_key} for group {group}")
    else:
        if not perms:
            print("Missing permission list, will grant ADMIN instead...")
            perms = ["admin"]
        new_group_perms = dict({"group": group}, **{p: True for p in perms})
        perm_obj["permissions"].append(new_group_perms)
        print(f"Granting {perms} to group {group} on project {project_key}...")
    prj.set_permissions(perm_obj)
