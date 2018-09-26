#!/usr/bin/env python

# 

""" 
This is compatible with API of DSS 4.X and DSS 5 
This tool comes with absolutely no maintenance 
"""

import sys
import time 
from datetime import datetime
ts = int("1284101485")

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
import os
import logging
import traceback
import urlparse
import pprint
        
import argparse

try:
    import dataiku # From inside DSS
except:
    import dataikuapi as dataiku # from outside DSS


DEBUG = False

def export_bundle(project,bundle_id,filePath):
    # Making sure parameter  type is the right one 
    assert type(project) == dataiku.dss.project.DSSProject,"project  as the wrong type {}".format(type(project))

    # make sure bundle doesn't exist
    if bundle_exists(project,bundle_id):
        raise ValueError("bundle is already imported on this project")  

    new_bundle = project.export_bundle(bundle_id)
    project.download_exported_bundle_archive_to_file(bundle_id,filePath)

    return

def deploy_bundle(project,bundle_id,filePath):
    # Making sure parameter  type is the right one 
    assert type(project) == dataiku.dss.project.DSSProject,"project  as the wrong type {}".format(type(project))
    assert os.path.exists(filePath)," Could not find bundle archive {}".format(filePath)
    # make sure  no bundle was imported yet

    if bundle_exists(project,bundle_id):
        raise ValueError("bundle is already imported on this project")
    # push bundle 
    logging.info("deploying bundle to automaation node")
    project.import_bundle_from_archive(filePath)
    return

def bundle_exists(project,bundle_id):
    for bundleDef in project.list_exported_bundles().get("bundles"):
        if bundle_id == bundleDef.get("bundleId"):
            return True
    return False
    
def canReachDSS(dssURL,client):
    response = client._session.get(urlparse.urljoin(dssURL, "/dip/api/ping")) 
    return response.status_code == 200



if __name__ == "__main__":

    # Parsing arguments for main
    parser = argparse.ArgumentParser(description="manage bundles ")
    parser.add_argument("action", choices=["create","deploy","download"], help="List of actions to execute")

    parser.add_argument("project",type=str,help="project id")
    parser.add_argument("-d","--dss-host", type=str, help="dataiku design or automaation instance (starting with http or https) ")

    parser.add_argument("-k","--api-key", type=str, default=None, help="The api key used to connect to DSS instance ")

    parser.add_argument("-b","--bundle-name", type=str, default=None, help="the bundile id ")
    parser.add_argument("-p","--bundle-path", type=str, default=None, help="the path of the bundle archive")
    parser.add_argument("--check-certificate", type=bool, default=True, help="check TLS certificate")
    parser.add_argument("--debug", type=bool, default=False, help="debug")

    args = parser.parse_args(sys.argv[1:])

    # initializing bundle details 
    bundle_id = args.bundle_name or "{}-v{}".format(args.project,str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')))
    bundle_full_path = args.bundle_path or os.path.join(os.path.abspath("."),bundle_id+".zip")
    dss_instance_url=args.dss_host# http(s)://your_server:yourdssport
    api_key=args.api_key# generated from  your user profile
    client=dataiku.DSSClient(dss_instance_url,api_key)

    project = client.get_project(args.project)
    client._session.verify = args.check_certificate # COMMENT THIS FOR  SSL CERTIFICATE CHECK 

    logging.basicConfig(level=logging.INFO)

    if "--debug" == args.debug:
        DEBUG = True
        logging.basicConfig(level=logging.DEBUG)
    # First check that DSS is reacheable 
    if not canReachDSS(dss_instance_url,client):
        logging.error("Can't reach DSS from {} , please check your URL ".format(dss_instance_url))
        raise OSError("DSS not reachable {} ".format(dss_instance_url))


    elif args.action == "create":
        bundle_id = args.bundle_name or "{}-v{}".format(args.project,str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')))
        bundle_full_path = args.bundle_path or os.path.join(os.path.abspath("."),bundle_id+".zip")
        logging.info("=== creating bundle...")

        export_bundle(project,bundle_id,bundle_full_path)
        logging.info("=== Done")
    elif args.action == "deploy":
        logging.info("=== deploying bundle...")
        deploy_bundle(project,args.bundle_name,args.bundle_path)
        logging.info("=== Done")
    elif args.action == "download":
        if not bundle_exists(project,args.bundle_name):
            raise ValueError("bundle doesn")
        bundle_full_path = args.bundle_path or os.path.join(os.path.abspath("."),args.bundle_name+".zip")
        project.download_exported_bundle_archive_to_file(args.bundle_name,bundle_full_path)

    


# END 
