# Maintaining a model per browser

In DSS, instances of a webapp share a Python backend, so that the webapp's view, preview in edit mode, and insights all make calls to the same Python process. To accomodate multi-user setups, the webapp code must handle coordination of models between the frontend side and the backend side, and the maintaining of a state on the backend side (if any). 


This sample code uses Flask's session mechanism to put a cookie that identifies the browser in which the webapp frontend is run. The backend maintains a model that mirrors the frontend's one, by aggregating changes sent by the frontend.

For all intents and purposes, this is equivalent to maintaining one model per user of the webapp.