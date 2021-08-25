def clear_tagged_datasets(client=None,
                          project_key=None,
                          tags=[],
                          filter="any",
                          dry_run=True):
    """Clear all datasets of a project that have specific tags.
    """

    project = client.get_project(project_key)
    to_clear = []
    for dataset in project.list_datasets():
        ds = project.get_dataset(dataset_name)
        if filter == "any":
            tag_intersection = list(set(tags) & set(dataset["tags"]))
            if tag_intersection:
                to_clear.append(ds)
        if filter == "all":
            # TODO Compare lists regardless of ordering
            if set(tags) == set(dataset["tags"]):
                to_clear.append(ds)
        print("The following datasets in project {} will be deleted:".format(project_key))
        for d in to_clear:
            print("- {}".format(ds.name))
