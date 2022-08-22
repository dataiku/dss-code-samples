import dataiku

from datetime import datetime
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_validate

def now_str() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")

 # !! - Replace these values with your own - !!
USER_PROJECT_KEY = ""
USER_XPTRACKING_FOLDER_ID = "" # 
USER_EXPERIMENT_NAME = ""
USER_TRAINING_DATASET= ""
USER_MLFLOW_CODE_ENV_NAME = ""


client = dataiku.api_client()
project = client.get_project(USER_PROJECT_KEY)

ds = dataiku.Dataset(USER_TRAINING_DATASET)
df = ds.get_dataframe()

# (1)
num_features = ['age', 'balance', 'duration', 'previous', 'campaign']
cat_features = ['job', 'marital', 'education', 'default',
                     'housing', 'loan', 'contact', 'poutcome']    
target = "y"
X_train = df.drop(target, axis=1)
y_train = df[target]

# (2)
num_pipeline = Pipeline([
    ('imp', SimpleImputer(strategy='median')),
    ('sts', StandardScaler()),
    ])

transformers = [
    ('num', num_pipeline, num_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ]
                                        
preprocessor = ColumnTransformer(transformers, remainder='drop')                                      

# (3)
param_space_rf = {
    "n_estimators": [40,80],
    "n_jobs": [-1],
    "max_depth": [6, 14],
    "min_samples_leaf": (10, 20, 40, 100)
}
n_cv_folds = 5
grid = ParameterGrid(param_space_rf)
cv = StratifiedKFold(n_splits=n_cv_folds)

# (4)
mf = project.get_managed_folder(USER_XPTRACKING_FOLDER_ID)
metrics = ["f1_macro", "roc_auc"]
mlflow_extension = project.get_mlflow_extension()
with project.setup_mlflow(mf) as mlflow:
    experiment_id = mlflow.create_experiment(f'{USER_EXPERIMENT_NAME}_{now_str()}')
    mlflow.tracking.MlflowClient().set_experiment_tag(experiment_id, "library", "Scikit-learn")
    mlflow.tracking.MlflowClient().set_experiment_tag(experiment_id, "predictionType", "BINARY_CLASSIFICATION")
    for hparams in grid:
        with mlflow.start_run(experiment_id=experiment_id) as run:
            print(f'Starting run {run.info.run_id} ...\n{hparams}')
            run_metrics = {}
            clf = RandomForestClassifier(**hparams)
            pipeline = make_pipeline(preprocessor, clf)
            scores = cross_validate(pipeline, X_train, y_train, cv=cv, scoring=metrics)
            
            # --Compute the mean and standard dev of the metrics across held-out folds
            for m in [f"test_{mname}" for mname in metrics]:
                run_metrics[f"mean_{m}"] = scores[m].mean()
                run_metrics[f"std_{m}"] = scores[m].std()    
            
            mlflow.log_metrics(metrics=run_metrics)
            
            for k,v in hparams.items():
                mlflow.log_param(k,v)
               
            # --Fit the prepocessing steps and the model on the whole train dataset
            pipeline.fit(X_train, y_train)
            
            # --Log the pipeline object 
            artifact_path = f"{type(clf).__name__}-{run.info.run_id}"
            mlflow.sklearn.log_model(sk_model=pipeline, artifact_path=artifact_path)
            
            # --Log useful information for the Dataiku Experiment tracking interface
            mlflow_extension.set_run_inference_info(run_id=run._info.run_id, 
                                                    prediction_type="BINARY_CLASSIFICATION", 
                                                    classes=pipeline.classes_.tolist(),                                  
                                                    code_env_name=USER_MLFLOW_CODE_ENV_NAME, 
                                                    target=target)
            print(f'Run {run.info.run_id} done\n{"-"*40}')
