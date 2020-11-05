import dataiku
from datetime import datetime


def list_jobs_by_status(client=None, project_key=None):
    """List jobs by current status in a given project.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key
    
    Returns:
        jobs_by_status: A dict of lists mapping jobs and their states
    """

    project = client.get_project(project_key)
    jobs_by_status = {"RUNNING": [],
                         "FAILED": [],
                         "DONE": [],
                         "ABORTED": []}
    for job in project.list_jobs():
        if not job["stableState"]:
            jobs_by_status["RUNNING"].append(job)
        else:
            jobs_by_status[job["state"]].append(job)
    return jobs_by_status


def filter_jobs_by_start_date(client=None, project_key=None, start_date=None):
    """List jobs that were started after a specific date.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key
        start_date: A string of the form 'YYYY/mm/dd' 

    Returns:
        jobs_after_start_date: A dict of lists mapping jobs and their states

    """
    jobs_by_status = list_jobs_by_status(client, project_key)
    start_date_timestamp = int(datetime.strptime(start_date, "%Y/%m/%d").strftime("%s")) * 1000
    is_after_start_date = lambda x, d: x["def"]["initiationTimestamp"] > d
    jobs_after_start_date = {_status: [job for job in _list if is_after_start_date(job, start_date_timestamp)] for _status, _list in jobs_by_status.items()}
    return jobs_after_start_date 


def abort_all_running_jobs(client=None, project_key=None):
    """Terminate all running jobs in a project.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key
    """

    project = client.get_project(project_key)
    aborted_jobs = []
    for job in project.list_jobs():
        if not job["stableState"]:
            job_id = job["def"]["id"]
            aborted_jobs.append(job_id)
            project.get_job(job_id).abort()
    print(f"Deleted {len(aborted_jobs)} running jobs")

