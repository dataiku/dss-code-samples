import dataiku

def list_connected_users(client=None):
    """List logged in users programmatically.

    :params client: A DSS client handle

    :return: A list of connected users
    :rtype: list
    """
    
    user_list = []
    dss_users = client.list_users()
    for user in dss_users:
        if user["activeWebSocketSessions"]!=0:
            user_list.append(user["displayName"])
    return user_list

