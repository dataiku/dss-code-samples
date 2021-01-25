- Build all
    ```python
    client = dataiku.api_client()
    project = client.get_project(dataiku.default_project_key())
    flow = project.get_flow()
    graph = flow.get_graph()
    for k,v in graph.data.get('nodes').items():
        if v.get('successors') == []:     
            definition = {
                "type" : 'RECURSIVE_BUILD',
                "outputs" : [{"id": k}]
            }
            print('Building dataset {}'.format(k)) 
            job = project.start_job(definition)
    ```
    Will need adjustments if there are saved models.

- Build specific tags only
- Build specific zones only
- Detect schema changes on a dataset and propagate them
  ```python
    settings = dataset.get_settings()
    settings.get_raw()["schema"] = {"columns":[]}
    settings.save()
    new_settings = dataset.autodetect_settings()
    new_settings.save()
```
