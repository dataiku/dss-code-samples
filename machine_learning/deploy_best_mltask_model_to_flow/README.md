# Deploy/upgrade best MLTask model to a project's Flow

## Question
* After training several models in a MLTask, I want to programmatically deploy the best one in a new saved model or update an existing model.

## Answers
The `deploy_with_best_model()` method creates a new saved model with the input MLTask's best model. The `update_with_best_model()` updates an existing saved model with the input MLTask's best model. Both rely on the [MLTask API](https://doc.dataiku.com/dss/latest/python-api/ml.html#interaction-with-a-ml-task) and saved model API. 
