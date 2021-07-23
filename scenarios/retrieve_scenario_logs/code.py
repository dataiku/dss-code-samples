import dataikuapi
import requests
import json

def retrieve_scenario_logs(host=None, project_api_key=None, project_key=None, run_id=None, scenario_id=None):
    """Return the logs of a given scenario.
    """ 
    url = "{}/public/api/projects/{}/scenarios/{}/{}/".format(host,project_key,scenario_id,run_id)
    response = requests.get(url, auth=(project_api_key, ''))
    if response.status_code == 200:
        json_string = json.dumps(response.json(), indent=2)
        return(json_string)
    else:
        return(str(response.status_code) + " status code; please check call details")


