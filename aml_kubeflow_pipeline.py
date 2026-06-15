from kfp import dsl
from kfp import compiler
from kfp.dsl import component
from kfp import kubernetes


# ----------------------------------
# Data Ingestion
# ----------------------------------
@component(
    base_image="python:3.11",
    packages_to_install=["pandas"]
)
def data_ingestion():

    import pandas as pd

    train = pd.read_csv("/data/aml_train.csv")
    test = pd.read_csv("/data/aml_test.csv")

    print("===== DATA INGESTION =====")
    print("Train Shape:", train.shape)
    print("Test Shape :", test.shape)


# ----------------------------------
# Data Validation
# ----------------------------------
@component(
    base_image="python:3.11",
    packages_to_install=["pandas"]
)
def data_validation():

    import pandas as pd

    df = pd.read_csv("/data/aml_train.csv")

    print("===== DATA VALIDATION =====")

    print("Null Count:",
          df.isnull().sum().sum())

    print("Duplicates:",
          df.duplicated().sum())

    if "Is_Laundering" not in df.columns:
        raise Exception(
            "Target column missing"
        )

    print("Validation Passed")


# ----------------------------------
# Feature Engineering
# ----------------------------------
@component(
    base_image="python:3.11",
    packages_to_install=["pandas"]
)
def feature_engineering():

    import pandas as pd

    df = pd.read_csv("/data/aml_train.csv")

    print("===== FEATURE ENGINEERING =====")

    print("Columns:")

    for col in df.columns:
        print(col)

    print("Feature Count:",
          len(df.columns)-1)


# ----------------------------------
# Train Model
# ----------------------------------
@component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas",
        "scikit-learn",
        "joblib"
    ]
)
def train_model():

    import pandas as pd
    import joblib

    from sklearn.ensemble import (
        RandomForestClassifier
    )

    train = pd.read_csv(
        "/data/aml_train.csv"
    )

    X = train.drop(
        "Is_Laundering",
        axis=1
    )

    y = train["Is_Laundering"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    model_path = f"/data/aml_model_{timestamp}.pkl"

    joblib.dump(model, model_path)

    print(f"Model Saved: {model_path}")


# ----------------------------------
# Evaluate
# ----------------------------------
@component(
    base_image="python:3.11",
    packages_to_install=[
        "pandas",
        "scikit-learn",
        "joblib"
    ]
)
def evaluate_model():

    import pandas as pd
    import joblib

    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score
    )

    model = joblib.load(
        "/data/aml_model.pkl"
    )

    test = pd.read_csv(
        "/data/aml_drift.csv"
    )

    X_test = test.drop(
        "Is_Laundering",
        axis=1
    )

    y_test = test[
        "Is_Laundering"
    ]

    pred = model.predict(
        X_test
    )

    print(
        "Accuracy:",
        accuracy_score(
            y_test,
            pred
        )
    )

    print(
        "Precision:",
        precision_score(
            y_test,
            pred
        )
    )

    print(
        "Recall:",
        recall_score(
            y_test,
            pred
        )
    )

    print(
        "F1:",
        f1_score(
            y_test,
            pred
        )
    )


# ----------------------------------
# Save Model
# ----------------------------------
@component(
    base_image="python:3.11"
)
def save_model():

    import os

    if os.path.exists(
        "/data/aml_model.pkl"
    ):
        print(
            "Model Saved Successfully"
        )
    else:
        raise Exception(
            "Model Not Found"
        )


# ----------------------------------
# Pipeline
# ----------------------------------
@dsl.pipeline(
    name="aml-final-pipeline"
)
def aml_pipeline():

    ingest = data_ingestion()

    validate = data_validation()
    validate.after(ingest)

    feature = feature_engineering()
    feature.after(validate)

    train = train_model()
    train.after(feature)

    evaluate = evaluate_model()
    evaluate.after(train)

    save = save_model()
    save.after(evaluate)

    for task in [
        ingest,
        validate,
        feature,
        train,
        evaluate,
        save
    ]:
        kubernetes.mount_pvc(
            task=task,
            pvc_name="aml-data-pvc",
            mount_path="/data"
        )


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=aml_pipeline,
        package_path="aml_kubeflow_pipeline.yaml"
    )
