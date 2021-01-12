import dataiku

client = dataiku.api_client()

project = client.get_project("PROJECT_KEY")
scenarios_list = project.list_scenarios()

new_recipient_email_address = "john.doe@here.com"

for scenario_metadata in scenarios_list:
    scenario = project.get_scenario(scenario_metadata['id'])
    scenario_definition = scenario.get_definition(with_status=False)

    update_scenario = False
    for i in range(0, len(scenario_definition['reporters'])):
        if scenario_definition['reporters'][i]['messaging']['type'] == "mail-scenario":
            recipients = [recipient.strip() for recipient in scenario_definition['reporters'][i]['messaging']['configuration']['recipient'].split(',')]
            if not new_recipient_email_address in recipients:
                recipients.append(new_recipient_email_address)
                scenario_definition['reporters'][i]['messaging']['configuration']['recipient'] = ', '.join(recipients)
                update_scenario = True
                print("Updating recipient for mail reporter \"{}\" of scenario \"{}\"".format(scenario_definition['reporters'][i]['name'], scenario_metadata['name']))
    if update_scenario:
        scenario.set_definition(scenario_definition,with_status=False)
