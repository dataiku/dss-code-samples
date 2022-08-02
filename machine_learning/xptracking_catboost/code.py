import dataiku
import mlflow
import mlflow.catboost
import pandas as pd
from catboost import CatBoostClassifier, Pool, cv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn import metrics
from dataikuapi.dss.ml import DSSPredictionMLTaskSettings

# !! - Replace these values by your own - !!
USER_PROJECT_KEY = "YOUR-PROJECT-KEY"
USER_XPTRACKING_FOLDER_ID = "YOUR-XP-TRACKING-FOLDER-ID"
USER_EXPERIMENT_NAME = "YOUR-EXPERIMENT-NAME"
USER_TRAINING_DATASET = "YOUR-TRAINING-DATASET-NAME"
USER_MLFLOW_CODE_ENV_NAME = "YOUR-MLFLOW-CODE-ENV-NAME"

client = dataiku.api_client()
project = client.get_project(USER_PROJECT_KEY)

# (1)
ds = dataiku.Dataset(USER_TRAINING_DATASET)
df = ds.get_dataframe()

cat_features= ["job", "marital", "education", "default", "housing","loan", "month", "contact", "poutcome"]
num_features= ["age", "balance", "day", "duration", "campaign"]
target_col ="y"
X = df.drop(target_col, axis=1)
y = LabelBinarizer().fit_transform(df[target_col[0]])

# (2)
params = {
    'iterations': 100,
    'learning_rate': 0.1, 
    'depth': 10,
    'cat_features': cat_features,
    'loss_function': 'Logloss',
    'eval_metric': 'AUC',
    'early_stopping_rounds': 5,
    'use_best_model': True,
    'random_seed': 42,
}

# (3)
mlflow_extension = project.get_mlflow_extension()
with project.setup_mlflow(managed_folder=USER_XPTRACKING_FOLDER_ID) as mlflow:
    mlflow.set_experiment(experiment_name=USER_EXPERIMENT_NAME)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        
        cv_dataset = Pool(
            data=X, label=y, cat_features= cat_features)

        scores = cv(cv_dataset,
                    params,
                    fold_count=5,
                    seed=42,
                    plot= False)
        
        for x in range(len(scores.index)):
            mlflow.log_metric(key='mean_AUC', value=scores['test-AUC-mean'][x], step=x+1)
            mlflow.log_metric(key='sd_AUC', value=scores['test-AUC-std'][x], step=x+1)

        mlflow.log_params(params=params)
        
        if params['early_stopping_rounds']:
            mlflow.log_metric(key='best_iteration', value=len(scores.index))
        
        if params['use_best_model']:
            params['iterations'] = len(scores.index)
            params['use_best_model'] = False

        model = CatBoostClassifier(**params)
        cb_model = model.fit(X,y)
        
        mlflow.catboost.log_model(cb_model, artifact_path="model")
    
        mlflow_extension.set_run_inference_info(run_id=run_id,
            prediction_type="BINARY_CLASSIFICATION",
            classes=['no', 'yes'],
            code_env_name=USER_MLFLOW_CODE_ENV_NAME,
            target=target_col)
