import dataiku
import json
from flask import request

TRUSTED_GROUP = "administrators"

@app.route('/get-sensitive-data')
def get_sensitive_data():
    headers = dict(request.headers)
    # Get the auth info of the user performing the request
    auth_info = dataiku.api_client().get_auth_info_from_browser_headers(headers)
    print ("User doing the query is %s" % auth_info["authIdentifier"])
    # If the user's group is not TRUSTED_GROUP, raise an exception
    if TRUSTED_GROUP not in auth_info["groups"] :
        raise Exception("You do not belong here, go away")
    else:
        data = {"status": "ok", "you_are": auth_info["authIdentifier"]}
    return json.dumps(data)