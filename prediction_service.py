from pathlib import Path

import joblib
import pandas as pd

from feature_engineering import create_features, get_model_input
from rule_engine import evaluate_rules


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "fraud_model.joblib"


def load_fraud_model():
    """Load and return the trained fraud-detection model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"The trained model was not found at: {MODEL_PATH}. "
            "Run 'python train_model.py' first."
        )

    return joblib.load(MODEL_PATH)


def validate_claim(claim: dict) -> list:
    """Validate claim fields and return a list of errors."""

    errors = []

    required_fields = [
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
    ]

    for field in required_fields:
        if field not in claim:
            errors.append(f"Missing required field: {field}")
        elif claim[field] is None or claim[field] == "":
            errors.append(f"Field cannot be empty: {field}")

    # Stop further validation if required fields are missing
    if errors:
        return errors

    try:
        customer_age = int(claim["customer_age"])

        if customer_age < 18 or customer_age > 100:
            errors.append(
                "Customer age must be between 18 and 100."
            )
    except (TypeError, ValueError):
        errors.append("Customer age must be a valid integer.")

    try:
        annual_premium = float(claim["annual_premium"])

        if annual_premium <= 0:
            errors.append(
                "Annual premium must be greater than zero."
            )
    except (TypeError, ValueError):
        errors.append("Annual premium must be numeric.")

    try:
        claim_amount = float(claim["claim_amount"])

        if claim_amount <= 0:
            errors.append(
                "Claim amount must be greater than zero."
            )
    except (TypeError, ValueError):
        errors.append("Claim amount must be numeric.")

    try:
        previous_claims = int(claim["previous_claims"])

        if previous_claims < 0:
            errors.append(
                "Previous claims cannot be negative."
            )
    except (TypeError, ValueError):
        errors.append(
            "Previous claims must be a valid integer."
        )

    try:
        vehicle_age = int(claim["vehicle_age"])

        if vehicle_age < 0:
            errors.append(
                "Vehicle age cannot be negative."
            )
    except (TypeError, ValueError):
        errors.append(
            "Vehicle age must be a valid integer."
        )

    policy_start_date = pd.to_datetime(
        claim["policy_start_date"],
        errors="coerce",
    )

    incident_date = pd.to_datetime(
        claim["incident_date"],
        errors="coerce",
    )

    claim_submission_date = pd.to_datetime(
        claim["claim_submission_date"],
        errors="coerce",
    )

    if pd.isna(policy_start_date):
        errors.append("Policy start date is invalid.")

    if pd.isna(incident_date):
        errors.append("Incident date is invalid.")

    if pd.isna(claim_submission_date):
        errors.append("Claim submission date is invalid.")

    if (
        not pd.isna(policy_start_date)
        and not pd.isna(incident_date)
        and incident_date < policy_start_date
    ):
        errors.append(
            "Incident date cannot be before the policy start date."
        )

    if (
        not pd.isna(incident_date)
        and not pd.isna(claim_submission_date)
        and claim_submission_date < incident_date
    ):
        errors.append(
            "Claim submission date cannot be before "
            "the incident date."
        )

    return errors


def get_risk_level(score: float) -> str:
    """Convert a numeric fraud score into a risk category."""

    if score >= 0.70:
        return "High"

    if score >= 0.40:
        return "Medium"

    return "Low"


def get_recommended_action(risk_level: str) -> str:
    """Return the recommended action for the risk category."""

    actions = {
        "Low": (
            "Continue standard claim processing, "
            "subject to normal verification."
        ),
        "Medium": (
            "Request additional supporting documents "
            "and conduct a secondary review."
        ),
        "High": (
            "Refer the claim for manual investigation "
            "before making a settlement decision."
        ),
    }

    return actions[risk_level]


def analyze_claim(claim: dict) -> dict:
    """Analyze one claim and return its fraud-risk result."""

    validation_errors = validate_claim(claim)

    if validation_errors:
        raise ValueError(" | ".join(validation_errors))

    model = load_fraud_model()

    claim_df = pd.DataFrame([claim])

    model_input = get_model_input(claim_df)

    probabilities = model.predict_proba(model_input)

    model_probability = float(probabilities[0][1])

    engineered_df = create_features(claim_df)
    engineered_claim = engineered_df.iloc[0].to_dict()

    rule_result = evaluate_rules(engineered_claim)

    rule_score = float(rule_result["rule_score"])

    final_score = (
        0.70 * model_probability
        + 0.30 * rule_score
    )

    final_score = round(
        min(max(final_score, 0.0), 1.0),
        4,
    )

    risk_level = get_risk_level(final_score)

    result = {
        "claim_id": claim["claim_id"],
        "model_probability": round(
            model_probability,
            4,
        ),
        "rule_points": rule_result["rule_points"],
        "rule_score": round(
            rule_score,
            4,
        ),
        "final_risk_score": final_score,
        "risk_percentage": round(
            final_score * 100,
            2,
        ),
        "risk_level": risk_level,
        "recommended_action": get_recommended_action(
            risk_level
        ),
        "reasons": rule_result["reasons"],
    }

    return result