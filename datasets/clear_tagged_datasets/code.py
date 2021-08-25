def clear_tagged_datasets(client=None,
                          project_key=None,
                          tags=[],
                          filter="any",
                          dry_run=True):
    """Clear all datasets of a project that have specific tags.

    :param client: A DSS client handle
    :param project_key: A string containing the project key
    :param tags: A list of tags to filter datasets on
    :param filter: If set to "any", clear datasets with at least one tag in the 'tags' param.
                   If set to "all", clear datasets with exactly all the tags in the 'tags' param.
    :param dry_run: If True, do not actually clear datasets.
    """

    project = client.get_project(project_key)
    to_clear = []
    for ds_item in project.list_datasets():
        if filter == "any":
            tag_intersection = list(set(tags) & set(ds_item["tags"]))
            if tag_intersection:
                to_clear.append(ds_item["name"])
        if filter == "all":
            if set(tags) == set(ds_item["tags"]):
                to_clear.append(ds_item["name"])
    print("The following datasets in project {} will be deleted:".format(project_key))
    for d in to_clear:
        d_str = "- {}".format(d)
        if not dry_run:
            project.get_dataset(d).clear()
        else:
            d_str += "(unchanged: dry run is True)"
        print(d_str)
