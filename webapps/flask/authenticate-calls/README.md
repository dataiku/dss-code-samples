# Authenticate users on a Flask webapp

In DSS, a webapp is accessible by default to user groups who have been authorized on its project. However, if the Python backend is enabled, then it can also retrieve information on the DSS user who is using the webapp. This allows for further customization in the webapp behavior depending on the user's identity.

The verification is done by the backend itself and is thus safe.

In this simple webapp example, if the user is part of the `TRUSTED_GROUP` group, clicking on the displayed button will pop an `alert()` in the browser, else a 500 error will be raised (check the backend logs).