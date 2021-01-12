# Machine learning

- [x] List all models and corresp. active version in a project
- [ ] "Pure code" model training and batch scoring in PyTorch
- [ ] "Pure code" model training and batch scoring in Tensorflow 2.x
- [ ] Custom model deployed on API service
- [ ] Visual ML: custom preprocessing (numerical + categorical)
- [ ] Visual ML: custom evaluation metric (classification + regression)
- [ ] Visual ML: custom Python model (classification + regression)
- [ ] Visual ML: download pre-trained model in a managed folder
- [ ] Retrieve and deploy the best model of a training session in the visual analysis
    ```
    import dataiku
client = dataiku.api_client()
project = client.get_project('YOUR_PROJECT_KEY')

analysis_id = 'k2BRw36W' # this can be found in the analysis URL or using project.list_analyses()
ml_taskid = 'aG8nyE8E' # this can be found in the mltask URL or using analysis.list_ml_tasks()
model_name = 'my_model' # name of the model that vill be deployed to flow
train_set = 'train' # name of my trainset

analysis = project.get_analysis(analysis_id)
mltask = analysis.get_ml_task(ml_taskid)
trained_models = mltask.get_trained_models_ids()
trained_models_snippets = [mltask.get_trained_model_snippet(model) for model in trained_models]
​
# Compare models to find the one you want to deploy, here we want to deploy the model with best r2 score
best_model = max(trained_models_snippets, key=lambda x:x['r2'])
# Deploy the best model to the flow, can also use mltask.redeploy_to_flow() to update an existing model
mltask.deploy_to_flow(best_model['fullModelId'], model_name, train_set )
```

