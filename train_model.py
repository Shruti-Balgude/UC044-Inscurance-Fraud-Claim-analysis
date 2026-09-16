import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from feature_engineering import get_model_input


DATA_PATH = Path("data/insurance_claims.csv")
MODEL_DIRECTORY = Path("models")
MODEL_PATH = MODEL_DIRECTORY / "fraud_model.joblib"
METADATA_PATH = MODEL_DIRECTORY / "model_metadata.json"

TARGET_COLUMN = "fraud_reported"

REQUIRED_COLUMNS = [
    "claim_id",
    "customer_age",
    "policy_type",
    "annual_premium",
    "claim_amount",
    "policy_start_date",
    "incident_date",
    "claim_submission_date",
    "incident_type",
    "incident_severity",
    "previous_claims",
    "police_report_available",
    "supporting_documents_available",
    "vehicle_age",
    "fraud_reported",
]


def validate_dataset(df: pd.DataFrame) -> None:
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The dataset is missing columns: "
            + ", ".join(missing_columns)
        )

    if df.empty:
        raise ValueError("The supplied dataset is empty.")

    target_values = set(df[TARGET_COLUMN].dropna().unique())

    if not target_values.issubset({0, 1}):
        raise ValueError(
            "fraud_reported must contain only 0 and 1."
        )


def create_preprocessor(
    X: pd.DataFrame,
) -> ColumnTransformer:
    numeric_columns = X.select_dtypes(
        include=["number"],
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        exclude=["number"],
    ).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent",
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                numeric_columns,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns,
            ),
        ]
    )


def calculate_metrics(
    model_name: str,
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "model": model_name,
        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "f1_score": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
        "confusion_matrix": confusion_matrix(
            y_test,
            predictions,
        ).tolist(),
    }

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)
    print(classification_report(y_test, predictions))
    print("ROC-AUC:", round(metrics["roc_auc"], 4))
    print("Confusion matrix:")
    print(metrics["confusion_matrix"])

    return metrics


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Place insurance_claims.csv inside data/."
        )

    df = pd.read_csv(DATA_PATH)

    validate_dataset(df)

    print("Dataset loaded successfully.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("\nFraud distribution:")
    print(df[TARGET_COLUMN].value_counts())

    X = get_model_input(df)
    y = df[TARGET_COLUMN].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    preprocessor = create_preprocessor(X_train)

    logistic_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    random_forest_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    max_depth=10,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\nTraining Logistic Regression...")
    logistic_pipeline.fit(X_train, y_train)

    logistic_metrics = calculate_metrics(
        model_name="Logistic Regression",
        pipeline=logistic_pipeline,
        X_test=X_test,
        y_test=y_test,
    )

    print("\nTraining Random Forest...")
    random_forest_pipeline.fit(X_train, y_train)

    random_forest_metrics = calculate_metrics(
        model_name="Random Forest",
        pipeline=random_forest_pipeline,
        X_test=X_test,
        y_test=y_test,
    )

    selected_pipeline = random_forest_pipeline
    selected_metrics = random_forest_metrics

    MODEL_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        selected_pipeline,
        MODEL_PATH,
    )

    metadata = {
        "selected_model": "Random Forest",
        "dataset_rows": len(df),
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
        "target": TARGET_COLUMN,
        "metrics": selected_metrics,
        "all_model_metrics": {
            "logistic_regression": logistic_metrics,
            "random_forest": random_forest_metrics,
        },
        "important_note": (
            "The supplied dataset is synthetic and the metrics "
            "must not be treated as real-world insurer performance."
        ),
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as metadata_file:
        json.dump(
            metadata,
            metadata_file,
            indent=4,
        )

    print("\nModel saved to:", MODEL_PATH)
    print("Metadata saved to:", METADATA_PATH)


if __name__ == "__main__":
    main()