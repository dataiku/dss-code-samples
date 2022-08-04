import dataiku
import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.model_selection import cross_validate, ParameterGrid, StratifiedKFold

# !! - Replace these values by your own - !!
USER_PROJECT_KEY = ""
USER_XPTRACKING_FOLDER_NAME = ""
USER_EXPERIMENT_NAME = ""
USER_TRAINING_DATASET = ""
USER_MLFLOW_CODE_ENV_NAME = ""

client = dataiku.api_client()
project = client.get_project(USER_PROJECT_KEY)

ds = dataiku.Dataset(USER_TRAINING_DATASET)
df = ds.get_dataframe()

# (1)
cat_features = ["job", "marital", "education", "default", "housing","loan", "month", "contact", "poutcome"]
num_features = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]
target ="y"

X = df.drop(target, axis=1)
y = df[target]

# (2)
num_pipeline = Pipeline([
         ("impute", SimpleImputer(strategy="median")),
         ("scale", StandardScaler())
     ])
     
cat_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
     transformers=[
         ("num", num_pipeline, num_features),
         ("cat", cat_transformer, cat_features),
     ],
     remainder="drop"
 )


# (3)
hparams_dict = {"learning_rate": [0.1, 0.05],
    "n_estimators": [10, 20],
    "seed": [47]
}

n_folds = 5
param_grid = ParameterGrid(hparams_dict)
cv = StratifiedKFold(n_splits=n_folds)

mlflow_extension = project.get_mlflow_extension()
with project.setup_mlflow(managed_folder=dataiku.Folder(USER_XPTRACKING_FOLDER_NAME).get_id()) as mlflow:
    mlflow.set_experiment(USER_EXPERIMENT_NAME)
    for hparams in param_grid:
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            
            clf_pipeline = Pipeline(steps=
                    [("preprocessor", preprocessor), 
                     ("classifier", LGBMClassifier(**hparams))
                    ])
            scores = cross_validate(clf_pipeline, X, y, cv=cv, scoring='roc_auc')

            run_metric_mean = scores['test_score'].mean()
            mlflow.log_metric('train_mean_auc', run_metric_mean)

            for k,v in hparams.items():
                mlflow.log_param(k,v)

            mlflow.sklearn.log_model(sk_model=clf_pipeline, artifact_path='model')
            
            mlflow_extension.set_run_inference_info(run_id=run_id,
                prediction_type="BINARY_CLASSIFICATION",
                classes=['no', 'yes'],
                code_env_name=USER_MLFLOW_CODE_ENV_NAME,
                target=target)

