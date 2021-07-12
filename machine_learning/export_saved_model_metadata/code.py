import dataiku
import copy
from dataiku import recipe

def export_saved_model_metadata(client=None, project_key=None, saved_model_id=None):
    """
    """

    project = client.get_project(project_key)
    model = project.get_saved_model(saved_model_id)
    output = []
    for version in model.list_versions():
        version_details = model.get_version_details(version["id"])
        version_dict = {}
    
        # Retrieve algorithm and hyperarameters
        resolved = copy.deepcopy(version_details.get_actual_modeling_params()["resolved"])
        version_dict["algorithm"] = resolved["algorithm"]
        del resolved["algorithm"]
        del resolved["skipExpensiveReports"]
        for (key, hyperparameters) in resolved.items():
            for (hyperparameter_key, hyperparameter_value) in hyperparameters.items():
                version_dict["hyperparameter_%s" % hyperparameter_key] = hyperparameter_value
            
        # Retrieve test performance
        for (metric_key, metric_value) in version_details.get_performance_metrics().items():
            version_dict["test_perf_%s" % metric_key] = metric_value
        
        # Retrieve lineage
        version_dict["training_target_variable"] = version_details.details["coreParams"]["target_variable"]
        split_desc = version_details.details["splitDesc"]
        version_dict["training_train_rows"] = split_desc["trainRows"]
        version_dict["training_test_rows"] = split_desc["testRows"]
        training_used_features = []
        for (key, item) in version_details.get_preprocessing_settings()["per_feature"].items():
            if item["role"] == "INPUT":
                training_used_features.append(key)
        version_dict["training_used_features"] = ",".join(training_used_features)
        
        # Retrieve training time
        ti = version_details.get_train_info()
        version_dict["training_total_time"] = int((ti["endTime"] - ti["startTime"])/1000)
        version_dict["training_preprocessing_time"] = int(ti["preprocessingTime"]/1000)
        version_dict["training_training_time"] = int(ti["trainingTime"]/1000)
    
        output.append(version_dict)

    return output
