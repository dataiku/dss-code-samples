import dataiku

def get_last_run_data(client=None, project_key=None, scenario_id=None):
    """Return the last run results of a given scenario.
    """

    prj = client.get_project(project_key)
    scn = prj.get_scenario(scenario_id)
    last_run = scn.get_last_finished_run()
    data = {"scenario_id": scenario_id,
            "outcome": last_run.outcome,
            "start_time": last_run.start_time.isoformat(),
            "end_time": last_run.end_time.isoformat()}
    return data

def get_all_last_runs(client=None):
    """Return the last run results for all scenarios of a DSS instance.
    """

    last_runs = []
    for prj_key in client.list_project_keys():
        prj = client.get_project(prj_key)
        for scn_id in [s["id"] for s in prj.list_scenarios()]:
            last_runs.append(get_last_run_data(client, prj_key, scn_id))
    return last_runs 

