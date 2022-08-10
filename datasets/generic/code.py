import dataiku
from dataikuapi.dss.dataset import DSSDataset, DSSDatasetSettings
from dataikuapi.dss.project import DSSProject, DSSProjectSettings


def get_dataset(dataset_name: str, client, project_key: str = None):
    """
    Get an existing dataset from the current project or a specified project

    :param str dataset_name: name of the dataset to retrieve
    :param client: dataiku client (generally dataiku.api_client())
    :param str project_key: The project key where the dataset is located.
        If None, the dataset is supposed to be located in the current project
        (where the function is run). (default to **None**)
    :return: the dataset if it exists, or None if it doesn't

    :note: don't forget to import :class:`dataikuapi.dss.dataset.DSSDataset`
    """
    if project_key:
        project = client.get_project(project_key)
    else:
        project = client.get_default_project()
    dataset: DSSDataset = project.get_dataset(dataset_name)
    if dataset.exists():
        return dataset
    else:
        return None


def dataset_promote_to_feature_group(dataset: DSSDataset):
    """
    Promote a dataset to a feature group

    :param dataset: the dataset to be promoted

    :note: don't forget to import :class:`dataikuapi.dss.dataset.DSSDataset`
        and :class:`dataikuapi.dss.dataset.DSSDatasetSettings`
    """
    settings: DSSDatasetSettings = dataset.get_settings()
    settings.set_feature_group(True)
    settings.save()


def dataset_add_tags(dataset: DSSDataset, tags: set):
    """
    Add tags to a dataset

    :param dataset: the dataset
    :param tags: a set of tags to be added to the existing tags,
        duplicate tags won't be added

    :note: don't forget to import :class:`dataikuapi.dss.dataset.DSSDataset`
        and :class:`dataikuapi.dss.dataset.DSSDatasetSettings`
    """
    settings: DSSDatasetSettings = dataset.get_settings()
    settings.tags = list(set(settings.tags()) | tags)
    settings.save()


def dataset_add_description(dataset: DSSDataset,
                            short_description: str = None,
                            long_description: str = None):
    """
    Add documentation (aka description) to a dataset

    :param dataset: the dataset
    :param short_description: short description to be added
        (default to **None**), keeps the old one if empty
    :param long_description: long description to be added
        (default to **None**), keeps the old one if empty

    :note: don't forget to import :class:`dataikuapi.dss.dataset.DSSDataset`
        and :class:`dataikuapi.dss.dataset.DSSDatasetSettings`
    """
    settings: DSSDatasetSettings = dataset.get_settings()
    if short_description:
        settings.short_description = short_description
    if long_description:
        settings.description = long_description
    settings.save()


def dataset_expose_to_project(dataset: DSSDataset,
                              external_project_key: str):
    """
    Expose a dataset to a project

    :param dataset: the dataset to expose
    :param external_project_key: where to expose it

    :note: don't forget to import :class:`dataikuapi.dss.project.DSSProject`,
    :class:`dataikuapi.dss.project.DSSProjectSettings`
    """
    current_project: DSSProject = dataset.project
    settings: DSSProjectSettings = current_project.get_settings()
    exposed_objects = settings.get_raw()['exposedObjects']
    for dss_object in exposed_objects['objects']:
        if (dss_object['type'] == 'DATASET') \
                and (dss_object['localName'] == dataset.dataset_name):
            not_found = True
            for rule in dss_object['rules']:
                if rule['targetProject'] == external_project_key:
                    not_found = False
            if not_found:
                dss_object['rules'].append({'targetProject': external_project_key,
                                            'appearOnFlow': True})
    settings.save()


def dataset_document_column(dataset: DSSDataset, name: str,
                            meaning: str = None,
                            comment: str = None):
    """
    Modify the meaning and/or comment of a column in the dataset

    :param dataset: the dataset to modify
    :param name: name of the column the user wants to modify
    :param meaning: the meaning of the column, if None/empty the previous
        meaning is kept (default to **None**)
    :param comment: the comment for the column, if None/empty the previous
        comment is kept (default to **None**)
    """
    schema: dict = dataset.get_schema()
    for col in schema['columns']:
        if col['name'] == name:
            if meaning:
                col['meaning'] = meaning
            if comment:
                col['comment'] = comment
    dataset.set_schema(schema)


def dataset_document_columns(dataset: DSSDataset,
                             columns: [(str, str, str)]):
    """
    Change the meaning and/or comment of some columns in the dataset
    :param dataset: the dataset to modify
    :param columns: an array of tuple representing the wanted modification.
        The tuple should have the form (name, meaning, comment).
        If meaning and/or comment are None/empty, the previous corresponding
        value is kept
    """
    schema: dict = dataset.get_schema()
    # first create an index to be able to grab the column faster
    indices = {}
    for x, col in enumerate(schema['columns']):
        indices[col['name']] = x
    # then modify each required column (that is present)
    for col in columns:
        (name, meaning, comment) = col
        if name in indices:
            index = indices[name]
            if meaning:
                schema['columns'][index]['meaning'] = meaning
            if comment:
                schema['columns'][index]['comment'] = comment
    dataset.set_schema(schema)
