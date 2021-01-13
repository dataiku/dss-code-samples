import dataiku

def get_best_model(client=None,
                   project_key=None,
                   analysis_id=None,
                   ml_task_id=None,
                   metric=None):
    """Return the 'best model' (according to the input metric) of a ML task.

    Args:
        client: A handle on the DSS instance
        project_key: A string representing the target project key
        analysis_id: A string linking to the target visual analysis.
                     Can be found in the analysis URL or via 
                     dataikuapi.dss.project.DSSProject.list_analyses()
        ml_task_id: A string linking to the target MLTask in a given analysis.
                   Can be found in the ML task URL or via
                   dataikuapi.dss.analysis.DSSAnalysis.list_ml_tasks()
        metric: A string defining which metric to use for performance ranking

    Returns:
        ml_task: A handle to interact with the ML task.
                 Useful when (re)deploying the model.
        best_model_snippet: A string containing the ID of the ML task's 'best model'

    """
    prj = client.get_project(project_key)
    analysis = prj.get_analysis(analysis_id)
    ml_task = analysis.get_ml_task(ml_task_id)
    trained_models = ml_task.get_trained_models_ids()
    trained_models_snippets = [ml_task.get_trained_model_snippet(m) for m in trained_models]
    # Assumes that for your metric, "higher is better"
    best_model_snippet = max(trained_models_snippets, key=lambda x:x[metric])
    best_model_id = best_model_snippet["fullModelId"]
    return ml_task, best_model_id


def deploy_with_best_model(client=None,
                           project_key=None,
                           analysis_id=None,
                           ml_task_id=None,
                           metric=None,
                           saved_model_name=None,
                           training_dataset=None):
    """Create a new Saved Model in the Flow with the 'best model' of a ML task.

    Args:
        client: A handle on the DSS instance
        project_key: A string representing the target project key.
        analysis_id: A string linking to the target visual analysis.
                     Can be found in the analysis URL or via 
                     dataikuapi.dss.project.DSSProject.list_analyses().
        ml_task_id: A string linking to the target MLTask in a given analysis.
                   Can be found in the ML task URL or via
                   dataikuapi.dss.analysis.DSSAnalysis.list_ml_tasks().
        metric: A string defining which metric to use for performance ranking.
        saved_model_name: A string to name the newly-created Saved Model.
        training_dataset: A string representing the name of the dataset
                          used as train set.

    """
    ml_task, best_model_id = get_best_model(client,
                                                 project_key,
                                                 analysis_id,
                                                 ml_task_id,
                                                 metric)
    ml_task.deploy_to_flow(best_model_id,
                           saved_model_name,
                           training_dataset)

def update_with_best_model(client=None,
                           project_key=None,
                           analysis_id=None,
                           ml_task_id=None,
                           metric=None,
                           saved_model_name=None,
                           activate=True):
    """Update an existing Saved Model in the Flow with the 'best model' 
       of a ML task.
    """
    ml_task, best_model_id = get_best_model(client,
                                            project_key,
                                            analysis_id,
                                            ml_task_id,
                                            metric)
    training_recipe_name = f"train_{saved_model_name}"
    ml_task.redeploy_to_flow(model_id=best_model_id,
                             recipe_name=training_recipe_name,
                             activate=activate)