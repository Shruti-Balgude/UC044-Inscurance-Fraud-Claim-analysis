import pandas as pd


DATE_COLUMNS = [
    "policy_start_date",
    "incident_date",
    "claim_submission_date",
]


MODEL_DROP_COLUMNS = [
    "claim_id",
    "policy_start_date",
    "incident_date",
    "claim_submission_date",
    "fraud_reported",
]


def create_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Create model-ready fraud-related features.

    The function does not modify the original DataFrame.
    """

    df = dataframe.copy()

    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            )

    required_date_columns = all(
        column in df.columns for column in DATE_COLUMNS
    )

    if required_date_columns:
        df["days_policy_to_incident"] = (
            df["incident_date"] - df["policy_start_date"]
        ).dt.days

        df["days_incident_to_submission"] = (
            df["claim_submission_date"] - df["incident_date"]
        ).dt.days

    if {
        "claim_amount",
        "annual_premium",
    }.issubset(df.columns):
        safe_premium = (
            pd.to_numeric(
                df["annual_premium"],
                errors="coerce",
            )
            .fillna(1)
            .clip(lower=1)
        )

        claim_amount = pd.to_numeric(
            df["claim_amount"],
            errors="coerce",
        )

        df["claim_to_premium_ratio"] = (
            claim_amount / safe_premium
        )

    if "police_report_available" in df.columns:
        df["police_report_missing"] = (
            df["police_report_available"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("no")
            .astype(int)
        )

    if "supporting_documents_available" in df.columns:
        df["documents_missing"] = (
            df["supporting_documents_available"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("no")
            .astype(int)
        )

    if "days_policy_to_incident" in df.columns:
        df["new_policy_claim"] = (
            df["days_policy_to_incident"] <= 30
        ).astype(int)

    if "claim_to_premium_ratio" in df.columns:
        df["high_claim_ratio"] = (
            df["claim_to_premium_ratio"] >= 8
        ).astype(int)

    if "previous_claims" in df.columns:
        previous_claims = pd.to_numeric(
            df["previous_claims"],
            errors="coerce",
        ).fillna(0)

        df["multiple_previous_claims"] = (
            previous_claims >= 3
        ).astype(int)

    if "days_incident_to_submission" in df.columns:
        df["late_submission"] = (
            df["days_incident_to_submission"] >= 21
        ).astype(int)

    return df


def get_model_input(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Create features and remove identifiers, dates and target columns.
    """

    engineered_df = create_features(dataframe)

    return engineered_df.drop(
        columns=MODEL_DROP_COLUMNS,
        errors="ignore",
    )