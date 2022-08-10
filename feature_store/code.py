import dataiku
from dataikuapi.dss.feature_store import DSSFeatureStore


def list_feature_group_name():
    """
    List all feature groups

    :return: All feature groups of the instance
    :rtype: array
    """
    client = dataiku.api_client()
    feature_store: DSSFeatureStore = client.get_feature_store()
    feature_groups: list = feature_store.list_feature_groups()

    result = []
    for feature_group in feature_groups:
        result.append({'project_key': feature_group.project_key,
                       'dataset_name': feature_group.name})
    return result


def collect_feature_group_with_meaning(meaning: str):
    """
    Collect all feature groups that have a column with a specific meaning

    :param str meaning: the meaning to search for
    :return: all feature groups that have a column with a specific meaning
    :rtype: array

    :note: this code use the function
        :meth:`../datasets/generic/get_dataset` and :meth:`list_feature_group_name`
    """
    result = []
    feature_groups = list_feature_group_name()
    for f in feature_groups:
        datas = get_dataset(f['dataset_name'],
                            dataiku.api_client(), f['project_key'])
        schema = datas.get_schema()
        for col in schema['columns']:
            if ('meaning' in col) and (col['meaning'] == meaning):
                result.append({'project_key': f['project_key'],
                               'dataset_name': f['dataset_name']})
    return result

