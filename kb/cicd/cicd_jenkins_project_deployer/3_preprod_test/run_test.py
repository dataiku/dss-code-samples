import dataikuapi


def test_run_scenario(params, scenario_id):
    print("*************************")
    print("Executing scenario ", scenario_id)
    client = dataikuapi.DSSClient(params["host"], params["api"])
    project = client.get_project(params["project"])
    scenario_result = project.get_scenario(scenario_id).run_and_wait()
    print("Scenario info: ", scenario_result.get_info())
    print("Scenario duration: ", scenario_result.get_duration())
    print(scenario_result.get_details()["scenarioRun"]["result"])
    print(scenario_result.get_details()["scenarioRun"]["result"]["outcome"])
    assert scenario_result.get_details()["scenarioRun"]["result"]["outcome"] == "SUCCESS"
