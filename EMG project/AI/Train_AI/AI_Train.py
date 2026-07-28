import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pickle
import numpy as np
import argparse
import sys

df = pd.read_csv(
    r"C:\Users\alifa\OneDrive\Documents\.vscode\VS CODE CODE\EMG project\AI\Data_Collector\emg_data.csv"
)

# Make sure the session column exists
if "session" not in df.columns:
    sys.exit("CSV does not contain a 'session' column.")

print(f"Number of sessions: {df['session'].nunique()}")

feature_columns = [
    'rms', 'std', 'min', 'max', 'mav',
    'wfl', 'aac', 'zc', 'wamp', 'afb'
]

X = df[feature_columns]
#X = df.drop(columns=["label", "session"])
y = df["label"]
groups = df["session"]



gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(gss.split(X, y, groups))

X_train = X.iloc[train_idx].copy()
X_test = X.iloc[test_idx].copy()

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

rest_sessions = df[df['label'] == 0]['session'].nunique()
moving_sessions = df[df['label'] == 1]['session'].nunique()

print(f"Rest sessions: {rest_sessions}")
print(f"Moving sessions: {moving_sessions}")
print()
print("Train sessions:", len(np.unique(groups.iloc[train_idx])))
print("Test sessions:", len(np.unique(groups.iloc[test_idx])))

model = None


def xgbAi():
    global model

    model = xgb.XGBClassifier(
        colsample_bytree=1.0,
        gamma=0.1,
        learning_rate=0.01,
        max_depth=7,
        n_estimators=300,
        subsample=0.7,
        random_state=42
    )

    model.fit(X_train, y_train)

    xgb.plot_importance(model)
    plt.show()


def forestAi():
    global model, X_train, X_test

    scaler = MinMaxScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("AI", choices=["xgb", "rfc"])

    args = parser.parse_args()

    if args.AI == "xgb":
        xgbAi()
    else:
        forestAi()

    y_pred = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(df["label"].value_counts())

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm).plot()
    plt.show()


if __name__ == "__main__":
    main()