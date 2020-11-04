import dataiku
import pandas as pd
from flask import request

@app.route('/get-sensitive-data')
def get_sensitive_data():
    request_headers = dict(request.headers)
    
    # Get the auth of the user performing the request
    # If the user is not authenticated, this will raise
    auth_info = dataiku.api_client().get_auth_info_from_browser_headers(request_headers)
    
    print ("User doing the query is %s" % auth_info["authIdentifier"])
    
    if not "trusted_people" in auth_info["groups"]:
        raise Exception("You do not belong here, go away")
        
    # Access the sensitive data
    # ...
    
    return json.dumps({"status": "ok", "you_are": auth_info["authIdentifier"]})