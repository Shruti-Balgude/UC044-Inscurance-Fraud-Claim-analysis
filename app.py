# from app.prediction_service import analyze_claim
from datetime import date, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from prediction_service import analyze_claim


st.set_page_config(
    page_title="ClaimShield AI",
    page_icon="🛡️",
    layout="wide",
)


def initialize_session_state() -> None:
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []


def risk_color(risk_level: str) -> str:
    colors = {
        "Low": "#22c55e",
        "Medium": "#f59e0b",
        "High": "#ef4444",
    }

    return colors.get(
        risk_level,
        "#64748b",
    )


def create_gauge(
    percentage: float,
    risk_level: str,
) -> go.Figure:
    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=percentage,
            number={
                "suffix": "%",
                "font": {
                    "size": 42,
                },
            },
            title={
                "text": "Combined Risk Score",
                "font": {
                    "size": 20,
                },
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                },
                "bar": {
                    "color": risk_color(risk_level),
                    "thickness": 0.3,
                },
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#dcfce7",
                    },
                    {
                        "range": [40, 70],
                        "color": "#fef3c7",
                    },
                    {
                        "range": [70, 100],
                        "color": "#fee2e2",
                    },
                ],
                "threshold": {
                    "line": {
                        "color": "#111827",
                        "width": 4,
                    },
                    "value": percentage,
                },
            },
        )
    )

    figure.update_layout(
        height=350,
        margin={
            "l": 30,
            "r": 30,
            "t": 70,
            "b": 20,
        },
    )

    return figure


initialize_session_state()

st.title("🛡️ ClaimShield AI")
st.subheader("Explainable Insurance Claim Fraud Risk Analysis")

st.info(
    "This demonstration estimates fraud risk for review purposes. "
    "It does not determine that a claimant committed fraud."
)

with st.sidebar:
    st.header("About this application")

    st.write(
        """
        This application combines:

        - A Random Forest machine-learning model
        - Configurable fraud-risk rules
        - Explainable risk indicators
        - A recommended review action
        """
    )

    st.divider()

    st.write("**Risk thresholds**")
    st.write("Low: below 40%")
    st.write("Medium: 40% to below 70%")
    st.write("High: 70% or above")

    st.divider()

    if st.button(
        "Clear prediction history",
        use_container_width=True,
    ):
        st.session_state.prediction_history = []
        st.success("History cleared.")


with st.form("claim_form"):
    st.header("Enter claim information")

    column1, column2, column3 = st.columns(3)

    with column1:
        claim_id = st.text_input(
            "Claim ID",
            value="CLM-DEMO-001",
        )

        customer_age = st.number_input(
            "Customer age",
            min_value=18,
            max_value=100,
            value=35,
        )

        policy_type = st.selectbox(
            "Policy type",
            options=[
                "Comprehensive",
                "Third Party",
                "Collision",
            ],
        )

        annual_premium = st.number_input(
            "Annual premium (INR)",
            min_value=1.0,
            value=25000.0,
            step=1000.0,
        )

        vehicle_age = st.number_input(
            "Vehicle age in years",
            min_value=0,
            max_value=40,
            value=5,
        )

    with column2:
        claim_amount = st.number_input(
            "Claim amount (INR)",
            min_value=1.0,
            value=80000.0,
            step=5000.0,
        )

        policy_start_date = st.date_input(
            "Policy start date",
            value=date.today() - timedelta(days=365),
        )

        incident_date = st.date_input(
            "Incident date",
            value=date.today() - timedelta(days=15),
        )

        claim_submission_date = st.date_input(
            "Claim submission date",
            value=date.today() - timedelta(days=10),
        )

        previous_claims = st.number_input(
            "Number of previous claims",
            min_value=0,
            max_value=20,
            value=0,
        )

    with column3:
        incident_type = st.selectbox(
            "Incident type",
            options=[
                "Collision",
                "Theft",
                "Fire",
                "Vandalism",
            ],
        )

        incident_severity = st.selectbox(
            "Incident severity",
            options=[
                "Minor",
                "Major",
                "Total Loss",
            ],
        )

        police_report_available = st.radio(
            "Police report available?",
            options=["Yes", "No"],
            horizontal=True,
        )

        supporting_documents_available = st.radio(
            "Supporting documents available?",
            options=["Yes", "No"],
            horizontal=True,
        )

    submitted = st.form_submit_button(
        "Analyze claim",
        type="primary",
        use_container_width=True,
    )


if submitted:
    # claim = {
    #     "claim_id": claim_id.strip(),
    #     "customer_age": int(customer_age),
    #     "policy_type": policy_type,
    #     "annual_premium": float(annual_premium),
    #     "claim_amount": float(claim_amount),
    #     "policy_start_date": policy_start_date.isoformat(),
    #     "incident_date": incident_date.isoformat(),
    #     "claim_submission_date": (
    #         claim_submission_date.isoformat()
    #     ),
    #     "incident_type": incident_type,
    #     "incident_severity": incident_severity,
    #     "previous_claims": int(previous_claims),
    #     "police_report_available": (
    #         police_report_available
    #     ),
    #     "supporting_documents_available": (
    #         supporting_documents_available
    #     ),
    #     "vehicle_age": int(vehicle_age),
    # }
    claim = {
    "claim_id": claim_id.strip(),
    "customer_age": int(customer_age),
    "policy_type": policy_type,
    "annual_premium": float(annual_premium),
    "claim_amount": float(claim_amount),
    "policy_start_date": policy_start_date.isoformat(),
    "incident_date": incident_date.isoformat(),
    "claim_submission_date": (
        claim_submission_date.isoformat()
    ),
    "incident_type": incident_type,
    "incident_severity": incident_severity,
    "previous_claims": int(previous_claims),
    "police_report_available": police_report_available,
    "supporting_documents_available": (
        supporting_documents_available
    ),
    "vehicle_age": int(vehicle_age),
    }

    try:
        result = analyze_claim(claim)

        st.session_state.prediction_history.append(
            {
                "Claim ID": result["claim_id"],
                "ML Probability": (
                    result["model_probability"]
                ),
                "Rule Score": result["rule_score"],
                "Final Risk Score": (
                    result["final_risk_score"]
                ),
                "Risk Level": result["risk_level"],
                "Recommended Action": (
                    result["recommended_action"]
                ),
            }
        )

        st.divider()
        st.header("Claim analysis result")

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "ML fraud probability",
            f"{result['model_probability'] * 100:.2f}%",
        )

        metric2.metric(
            "Rule score",
            f"{result['rule_points']} / 100",
        )

        metric3.metric(
            "Final risk score",
            f"{result['risk_percentage']:.2f}%",
        )

        metric4.metric(
            "Risk category",
            result["risk_level"],
        )

        left_column, right_column = st.columns(
            [1.2, 1]
        )

        with left_column:
            st.plotly_chart(
                create_gauge(
                    result["risk_percentage"],
                    result["risk_level"],
                ),
                use_container_width=True,
            )

        with right_column:
            st.subheader(
                f"{result['risk_level']} risk"
            )

            if result["risk_level"] == "High":
                st.error(
                    "This claim contains strong risk indicators "
                    "and should receive manual review."
                )

            elif result["risk_level"] == "Medium":
                st.warning(
                    "This claim contains indicators that require "
                    "additional verification."
                )

            else:
                st.success(
                    "No strong risk indicators were identified by "
                    "the current demonstration configuration."
                )

            st.markdown("### Recommended action")
            st.write(
                result["recommended_action"]
            )

        st.markdown("### Risk indicators")

        for reason in result["reasons"]:
            st.write(f"• {reason}")

        st.caption(
            "The model and rule thresholds are for educational "
            "demonstration. An authorized reviewer should verify "
            "the original claim information before any decision."
        )

    except FileNotFoundError as error:
        st.error(str(error))
        st.info(
            "Run `python train_model.py` in the VS Code "
            "terminal and try again."
        )

    except ValueError as error:
        st.error(f"Invalid claim information: {error}")

    except Exception as error:
        st.error(
            "The claim could not be analyzed."
        )
        st.exception(error)


if st.session_state.prediction_history:
    st.divider()
    st.header("Current session history")

    history_df = pd.DataFrame(
        st.session_state.prediction_history
    )

    display_df = history_df.copy()

    for column in [
        "ML Probability",
        "Rule Score",
        "Final Risk Score",
    ]:
        display_df[column] = display_df[column].map(
            lambda value: f"{value * 100:.2f}%"
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = history_df.to_csv(
        index=False,
    ).encode("utf-8")

    st.download_button(
        label="Download prediction history",
        data=csv_data,
        file_name="claim_prediction_history.csv",
        mime="text/csv",
    )