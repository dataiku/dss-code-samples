client = dataiku.api_client()
project_name = YOUR_PROJECT_HERE

proj = client.get_project(project_name)
jobs = proj.list_jobs()
datasets = proj.list_datasets() 

def job_modifies_dataset(job, dataset_name, build_start_date):
    if job['startTime'] <= build_start_date <= job['endTime']: # check that the jobs start and end were around the dataset
        for output in job['def']['outputs']: # check that the dataset was modified by the job
            if output['targetDataset'] == dataset_name:
                return True
    return False

for d in datasets:
    dataset = proj.get_dataset(d['name'])
    metrics = dataset.get_last_metric_values()
    for metric in metrics.raw['metrics']:
        if metric['metric']['metricType'] == 'BUILD_START_DATE':
            info = {'ds_name'     : d['name'], 
                    'computed'    : metric['lastValues'][0]['computed'],
                    'build_start' : metric['lastValues'][0]['value']
                   }
            for job in jobs:
                if job_modifies_dataset(job, info['ds_name'], info['computed']):
                    info['initiator'] = job['def']['initiator']

print info
