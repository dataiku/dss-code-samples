import dataiku

def list_logged_in_users(client=None):
    """List logged in users programmatically.
    """
    
    user_list = []
    dss_users = client.list_users()
    for user in dss_users:
        if user["activeWebSocketSessions"]!=0:
            user_list.append(user["displayName"])
    return user_list

