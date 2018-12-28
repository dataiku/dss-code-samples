# Maintaining a model per frontend

In DSS, instances of a webapp share a Python backend, so that the webapp's view, preview in edit mode, and insights all make calls to the same Python process. To accomodate multi-user setups, the webapp code must handle coordination of models between the frontend side and the backend side, and the maintaining of a state on the backend side (if any). 


This sample code makes the frontend generate an identifier so that the backend can maintain one model for each frontend. The backend maintains a model that mirrors the frontend's one, by aggregating changes sent by the frontend.
