import lightgbm as lgbm

clf = lgbm.LGBMModel(
    boosting_type = 'gbdt',
    objective = 'regression',
    n_estimators = 300,
    num_boost_round = 200000,
    num_leaves = 30,
    learning_rate = 0.05,
    min_split_gain = 0.25,
    min_child_weight =  1,
    min_child_samples = 10,
    scale_pos_weight = 1,
    seed = 42,
    max_depth = -1,
    subsample = 0.8,
    bagging_fraction = 1,
    max_bin = 5000,
    bagging_freq = 20,
    colsample_bytree = 0.6,
    metric = "rmse",
    n_jobs = 10,
    silent = False
)
