#!/usr/bin/python
# Author joel.belafa@dataiku.com
# Thanks to ppelissier for raising this  question

""" 

This is compatible with API of DSS 4.X  and DSS 5 
This tool comes with absolutely no maintenance 

"""

import sys
import time
import dataikuapi
import os
import logging


dss_instance_url="http://localhost:21100" # http(s)://your_server:yourdssport
api_key="TmRB3MFZQph3BTLR2dqtDtwXifqMV9cV" # generated from  your user profile
client=dataikuapi.DSSClient(dss_instance_url,api_key)

class MigrationException (Exception):
    pass



def patch_project(project):
    
    assert type(project) == dataikuapi.dss.project.DSSProject,"project  as the wrong type {}".format(type(project))

    logging.info("patching post MUS ")
    for recipeDef in project.list_recipes():
        recipe = project.get_recipe(recipeDef.get("name"))
        definition = recipe.get_definition_and_payload()
        try:
            logging.info("trying  method A - expecting definition and payload handling ")
            try:
                json_definition = definition.get_json_payload()
            except ValueError:
                raise MigrationException("Migration method not applicable")

            # Patch hive engine and  disable dataiku UDF 
            json_definition.get("engineParams").get("hive")["executionEngine"]="HIVESERVER2"
            json_definition.get("engineParams").get("hive")["addDkuUdf"] = False

            # update JsonDefinition
            definition.set_json_payload(json_definition)
        except MigrationException :
            logging.info("trying  method A failed ")
            logging.info("trying  method B")

            json_definition = definition.get_recipe_raw_definition()
            json_definition["params"]["executionEngine"]="HIVESERVER2"
            json_definition["params"]["addDkuUdf"]=False
            definition.set_json_payload(json_definition)

        recipe.set_definition_and_payload(definition)
    ogging.info("project patched successfully")

    return 



def main(client):
    
    for projectDef  in  client.list_projects():
        projectKey = projectDef.get("projectKey")
        project = client.get_project(projectKey)
        try:
            patch_project(project)
        except 










client=dataikuapi.DSSClient(dss_instance_url,api_key)