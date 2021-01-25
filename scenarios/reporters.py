import dataiku

def add_email_recipients(client=None, project_key=None, scenario_ids=[], recipients=[]):
    """Append additional recipients to scenario email reporters.

    Args:
        client: A handle on the target DSS instance
        project_key: A string representing the target project key
        scenario_ids: A list of scenario ID strings
        recipients: A list of email address strings
        
    """

    prj = client.get_project(project_key)
    if not scenario_ids:
        print("No scenario id specified, will apply to ALL scenarios")
        scenario_ids = [scn["id"] for scn in prj.list_scenarios()]
    for scn_id in scenario_ids:
        handle = prj.get_scenario(scn_id)
        settings = handle.get_settings()
        reporters = settings.raw_reporters
        if not reporters:
            print("No reporter found.")
        else:
            for rep in reporters:
                if rep["messaging"]["type"] == "mail-scenario":
                    if rep["messaging"]["configuration"]["recipient"]:
                        sep = ', '
                    else:
                        sep = ''
                    rep["messaging"]["configuration"]["recipient"] += (sep + ', '.join(recipients))
            settings.save()
