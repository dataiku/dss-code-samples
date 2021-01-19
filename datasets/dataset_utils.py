import dataiku 
from datetime import datetime

def get_last_build_date(client=None, project_key=None, dataset=None):
    """Returns a datetime onject representing the last time an output
    dataset was built.
    Args:
        client: A handle on the target DSS instance.
        project_key: A string representing the target project key.
        dataset: name of dataset,
    """
	dataset_info = dataiku.Dataset("test_append").get_files_info()
	last_modif = dataset_info.get("globalPaths")[0].get("lastModified")
	dt = datetime.fromtimestamp(last_modif/1000)
	return dt

def build_todays_partition(client=None, project_key=None, dataset=None):
	 """Build parition of today's date in specified dataset.
	 Return status of build. 
    Args:
        client: A handle on the target DSS instance.
        project_key: A string representing the target project key.
        dataset: name of dataset,
    """
	now = datetime.now()
	partition = now.strftime("%Y-%m-%d")
	project = client.get_project(project_key)
	dataset = project.get_dataset(dataset)
	job = dataset.build(partitions=partition)
	return job.get_status()


