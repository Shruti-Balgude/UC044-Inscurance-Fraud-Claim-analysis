def evaluate_rules(claim: dict) -> dict:
    """
    Evaluate demonstration insurance fraud-risk rules.

    The rules and points are intended for educational use.
    A real insurance organization would configure its own
    rules, thresholds, and review process.
    """

    points = 0
    reasons = []

    # Read numeric values safely
    days_policy_to_incident = int(
        claim.get("days_policy_to_incident", 9999)
    )

    days_incident_to_submission = int(
        claim.get("days_incident_to_submission", 0)
    )

    claim_to_premium_ratio = float(
        claim.get("claim_to_premium_ratio", 0)
    )

    previous_claims = int(
        claim.get("previous_claims", 0)
    )

    # Read text values safely and normalize capitalization
    incident_type = str(
        claim.get("incident_type", "")
    ).strip().lower()

    police_report_available = str(
        claim.get("police_report_available", "yes")
    ).strip().lower()

    supporting_documents_available = str(
        claim.get(
            "supporting_documents_available",
            "yes",
        )
    ).strip().lower()

    # Rule 1: Incident occurred shortly after policy activation
    if days_policy_to_incident <= 30:
        points += 20
        reasons.append(
            "The incident occurred within 30 days "
            "of policy activation."
        )

    # Rule 2: Claim amount is high compared with premium
    if claim_to_premium_ratio >= 8:
        points += 20
        reasons.append(
            "The claim amount is at least eight times "
            "the annual premium."
        )

    # Rule 3: Claimant has several previous claims
    if previous_claims >= 3:
        points += 15
        reasons.append(
            "The claimant has three or more previous claims."
        )

    # Rule 4: Theft claim has no police report
    if (
        incident_type == "theft"
        and police_report_available == "no"
    ):
        points += 25
        reasons.append(
            "A police report is unavailable for a theft claim."
        )

    # Rule 5: Supporting documents are unavailable
    if supporting_documents_available == "no":
        points += 10
        reasons.append(
            "Supporting documents are unavailable."
        )

    # Rule 6: Claim was submitted late
    if days_incident_to_submission >= 21:
        points += 10
        reasons.append(
            "The claim was submitted 21 or more days "
            "after the incident."
        )

    # Do not allow the rule points to exceed 100
    limited_points = min(points, 100)

    if not reasons:
        reasons.append(
            "No major demonstration rules were triggered."
        )

    return {
        "rule_points": limited_points,
        "rule_score": limited_points / 100,
        "reasons": reasons,
    }