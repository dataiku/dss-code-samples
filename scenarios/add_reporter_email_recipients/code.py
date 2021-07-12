def add_reporter_email_recipients(client=None,
                                  project_key=None,
                                  scenario_id=None,
                                  recipients=[]):
    """Append additional recipients to a scenario email reporter.
    """

    prj = client.get_project(project_key)
    scn_settings = prj.get_scenario(scenario_id).get_settings()
    reporters = scn_settings.raw_reporters
    if not reporters:
        print("No reporter found, will do nohting.")
    else:
        for rep in reporters:
            messaging = rep["messaging"]
            if messaging["type"] == "mail-scenario":
                if messaging["configuration"]["recipient"]:
                    sep = ', '
                else:
                    sep = ''
                messaging["configuration"]["recipient"] += (sep + ', '.join(recipients))
    scn_settings.save()
