# List logged in users programmatically

## Question
I want to know which users are logged in to an instance to figure out if the instance can be stopped.

## Answer
This is possible by using the [`list_users()`](https://doc.dataiku.com/dss/latest/python-api/users-groups.html) method of the DSS public API. That method returns a value for `activeWebSocketSessions` which indicates the number of DSS sessions that a user is logged into at the moment. Anything other than 0 indicates that a user is connected to the DSS instance.
