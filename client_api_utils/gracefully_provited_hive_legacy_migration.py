#!/usr/bin/env python

# Thanks to Pierre Pelissier for raising this question

""" 
This is compatible with API of DSS 4.X and DSS 5 
This tool comes with absolutely no maintenance 
"""

import sys
import time 

import os
import logging
import traceback
import requests
from requests import Session
import urlparse
import pprint
        

try:
    import dataiku # From inside DSS
except:
    import dataikuapi as dataiku # from outside DSS

class MigrationException (Exception):
    pass

DEBUG = False

def patch_project(project):
    # Making sure parameter  type is the right one 
    assert type(project) == dataiku.dss.project.DSSProject,"project  as the wrong type {}".format(type(project))



    logging.info("patching post MUS ")
    to_check = False
    for recipeDef in project.list_recipes():
        recipe = project.get_recipe(recipeDef.get("name"))
        definition = recipe.get_definition_and_payload()
        if DEBUG:
            print "DEF BEFORE"
            pprint.pprint(definition.data)
            print "============="
        # This try/except block aims to migrate hive settings using 2 different methods
        logging.info("patching recipe {}".format(recipeDef.get("name")))
        try:
            logging.info("trying  method A - expecting definition and payload handling ")
            json_definition = None
            try:
                # success of the following call validates use of methode A 
                json_definition = definition.get_json_payload()

                # Patch hive engine and  disable dataiku UDF
                try:
                    if str(json_definition.get("engineParams").get("hive").get("executionEngine")).startswith("HIVECLI") :
                        json_definition.get("engineParams").get("hive")["executionEngine"]="HIVESERVER2"
                        json_definition.get("engineParams").get("hive")["addDkuUdf"] = False
                        definition.set_json_payload(json_definition)
                except:
                    pass
            except  Exception as e :
                print e.message
                raise MigrationException("Migration method not applicable")

        except :
            try:
                logging.info("trying  method A failed ")
                logging.info("trying  method B")
                
                recipe_def = definition.get_recipe_raw_definition()
                if str(recipe_def.get("params").get("executionEngine")).startswith("HIVECLI"):
                    recipe_def["params"]["executionEngine"]= "HIVESERVER2"
                recipe_def["params"]["addDkuUdf"]=False
                definition.data["recipe"] = recipe_def
            except Exception as e :
                traceback.print_exception(*sys.exc_info())
                to_check = True
                logging.error("Please check recipe : "+recipeDef.get("name"))

        if DEBUG:
            print "DEF AFTER "
            pprint.pprint(definition.data)
        if not definition.data.get("payload") :
            definition.data["payload"] = "{}"
        recipe.set_definition_and_payload(definition)

    logging.info("project patched successfully")

    return to_check

def canReachDSS(dssURL):
    request = requests.get(urlparse.urljoin(dssURL, "/dip/api/ping"))
    return request.status_code == 200



def main(client):
    
    projects_migrated = []
    projects_to_check = []
    for projectDef  in  client.list_projects(): 
        project = client.get_project(projectDef.get("projectKey"))
        if patch_project(project) :
            projects_migrated.append(project.project_key)
        else:
            logging.error(" error(s) in  project : {}".format(project.project_key))
            projects_to_check.append(project.project_key)

    print "PROJECTS MIGRATED :"
    print "\t{}".format("\n\t".join(projects_migrated))
    print "PROJECTS TO CHECK (experiening issue) :"
    print "\t{}".format("\n\t".join(projects_to_check))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 3:
        print "wrong number of arguments "+ str(len(sys.argv))
        print "USAGE  :{} [--debug]  DSS_INSTANCE_FULL_HTTP_ROOT_URL API_KEY".format(sys.argv[0])
        exit(1)

    if "--debug" in sys.argv:
        DEBUG = True
        sys.argv.remove("--debug")
        logging.basicConfig(level=logging.DEBUG)

    dss_instance_url=sys.argv[1]# http(s)://your_server:yourdssport
    api_key=sys.argv[2]# generated from  your user profile
    client=dataiku.DSSClient(dss_instance_url,api_key)
    client._session.verify = False # COMMENT THIS FOR  SSL CERTIFICATE CHECK 

    # First check that DSS is reacheable 
    if not canReachDSS(dss_instance_url):
        logging.error("Can't reach DSS from {} , please check your URL ".format(dss_instance_url))
        raise OSError("DSS not reachable {} ".format(dss_instance_url))

    main(client)


# END 
