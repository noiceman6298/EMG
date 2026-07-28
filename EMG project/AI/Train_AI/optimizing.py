import xgboost as xgb
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import GridSearchCV
import sys

df = pd.read_csv(r'')
# Make sure the session column exists
if "session" not in df.columns:
    sys.exit("CSV does not contain a 'session' column.")

print(f"Number of sessions: {df['session'].nunique()}")

X = df.drop(columns=["label", "session"])
y = df["label"]
groups = df["session"]

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.3,
    random_state=42
)

train_idx, test_idx = next(gss.split(X, y, groups))

X_train = X.iloc[train_idx].copy()
X_test = X.iloc[test_idx].copy()

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

param_grid = {
    "n_estimators": [100, 300, 500],
    "max_depth": [3, 5, 7],
    "learning_rate": [0.01, 0.05, 0.1],
    "subsample": [0.7, 1.0],
    "colsample_bytree": [0.8, 1.0],
    "gamma": [0, 0.1],
}

"""
param_grid = { 
    "n_estimators": [50, 100, 300, 500, 700], 
    "max_depth": [3, 5, 7], 
    "learning_rate": [0.01, 0.1], 
    "subsample": [0.7, 1.0], 
    "colsample_bytree": [0.7, 1.0], 
    "gamma": [0, 0.1], 
    "lambda": [1, 2], 
    "alpha": [0, 1] 
}

"""


xgb_model = xgb.XGBClassifier()

grid_search = GridSearchCV(estimator= xgb_model, param_grid= param_grid, scoring= "accuracy", cv= 3, verbose= 1)

grid_search.fit(X_train, y_train)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Best Score: {grid_search.best_score_}")
