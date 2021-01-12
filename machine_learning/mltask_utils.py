import dataiku

def deploy_best_model(client=None,
                   project_key=None,
                   analysis_id=None,
                   mltask_id=None,
                   metric=None):
    """Deploy the best model (according to the input metric) of a mltask to the flow.

    Args:
        client: A handle on the DSS instance
        project_key: A string representing the target project key
        analysis_id: A string linking to the target visual analysis
        mltask_id: A string linking to the target mltask in a given analysis
        metric: A string defining which metric to use for performance ranking

    Returns:
    """
    # WIP 
    prj = client.get_project(project_key)
    analysis = prj.get_analysis(analysis_id)
    mltask = analysis.get_ml_task(mltask_id)
    trained_models = mltask.get_trained_models_ids()
    trained_models_snippets = [mltask.get_trained_model_snippet(m) for m in trained_models]
    best_model = max(trained_models_snippets, key=lambda x:x[metric])
    return best_model 






