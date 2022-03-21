import dataiku

def abort_all_running_jobs(client=None, project_key=None):
    """Terminate all running jobs in a project.

    :param client: A DSS client handle
    :param project_key: A string containing the project key

    """

    project = client.get_project(project_key)
    aborted_jobs = []
    for job in project.list_jobs():
        if not job["stableState"]:
            job_id = job["def"]["id"]
            aborted_jobs.append(job_id)
            project.get_job(job_id).abort()
    print(f"Deleted {len(aborted_jobs)} running jobs")

