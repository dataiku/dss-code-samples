import dataiku
from datetime import datetime

def list_jobs_by_status(client=None, project_key=None):
    """
    """

    project = client.get_project(project_key)
    jobs_by_status = {"RUNNING": [],
                         "FAILED": [],
                         "DONE": [],
                         "ABORTED": []}
    for job in project.list_jobs():
        if "state" not in job:
            jobs_by_status["RUNNING"].append(job)
        else:
            jobs_by_status[job["state"]].append(job)
    return jobs_by_status


def filter_jobs_by_start_date(jobs_by_status=None, start_date=None):
    """
    """

    start_date_timestamp = int(datetime.strptime(start_date, "%Y/%m/%d").strftime("%s")) * 1000
    is_after_start_date = lambda x, d: x["def"]["initiationTimestamp"] > d
    jobs_after_start_date = {_status: [job for job in _list if is_after_start_date(job, start_date_timestamp)] for _status, _list in jobs_by_status.items()}
    return jobs_after_start_date 


