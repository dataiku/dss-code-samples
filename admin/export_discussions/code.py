import dataiku

def get_discussions_from_object(object_handle=None):
    """Return all discussion messages from a commentable object.

    :param object_handle: The API handle of the target commentable object

    :returns: A list of discussions with all their respective message data
    :rtype: list
    """
    
    disc_data = []
    discussions = object_handle.get_object_discussions()
    for disc in discussions.list_discussions():
        disc_content = {}
        disc_content["topic"] = disc.get_metadata()["topic"]
        msg_list = []
        for msg in disc.get_replies():
            msg_content = {}
            msg_content["author"] = msg.get_author()
            msg_content["ts"] = msg.get_timestamp()
            msg_content["text"] = msg.get_text()
            msg_list.append(msg_content)
        disc_content["messages"] = msg_list
        disc_data.append(disc_content)
    return disc_data

        
def export_project_discussions(client=None, project_key=None):
    """Return all discussion data for a given Project.

    :param client: A DSS client handle
    :param project_key: A string containing the project key

    :returns: A dictionary mapping each commentable object type to a list of discussions.
    :rtype: dict
    """
    proj_disc = {}
    project = client.get_project(project_key)
    dispatch = {
        "datasets": {
            "f_list": project.list_datasets, 
            "f_get": project.get_dataset
        },
        "recipes": {
            "f_list": project.list_recipes,
            "f_get": project.get_recipe
        },
        "scenarios": {
            "f_list": project.list_scenarios,
            "f_get": project.get_scenario
        },
        "managed_folders": {
            "f_list": project.list_managed_folders,
            "f_get": project.get_managed_folder
        }
    }
    
    for obj_type, funcs in dispatch.items():
        obj_disc = []
        for item in funcs["f_list"]():
            disc = {}
            disc["name"] = item["name"]
            obj_handle = funcs["f_get"](item["name"])
            disc["discussions"] = get_discussions_from_object(obj_handle)
            obj_disc.append(disc)
        proj_disc[obj_type] = obj_disc
        
    # Special case: project discussions
    proj_disc["project"] = get_discussions_from_object(project)
    
    # Special case: wiki
    wiki_disc = []
    articles = project.get_wiki().list_articles()
    for art in articles:
        art_disc = {}
        art_disc["article_id"] = art.article_id
        art_disc["discussions"] = get_discussions_from_object(art)
        wiki_disc.append(art_disc)
    proj_disc["wiki"] = wiki_disc
    
    return proj_disc
