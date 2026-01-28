
# Streamlit Application Specification: AI Model Inherent Risk Self-Assessment

## 1. Application Overview

The **AI Model Inherent Risk Self-Assessment** application provides a streamlined workflow for a **Model/System Owner** at Apex Financial Services to register new AI models and conduct an initial inherent risk self-assessment. This process is crucial for aligning with the Model Risk Management (MRM) framework, particularly the principles outlined in **SR Letter 11-7**, which emphasizes robust model development, implementation, use, and comprehensive governance.

**High-level Story Flow:**

1.  **Model Registration:** The Model Owner begins by entering essential metadata about their new AI model (e.g., a Predictive Maintenance Model) into a structured form. This input includes details like the model's business use, technical characteristics, and key risk factors (e.g., decision criticality, data sensitivity). Upon submission, the application automatically generates a unique Model ID and captures audit information. Crucially, it then uses the provided metadata to calculate a preliminary inherent risk score and assigns a proposed risk tier based on Apex Financial Services' internal scoring framework.
2.  **Risk Score Preview:** After registration, the Model Owner navigates to a dedicated page to review the calculated inherent risk score and proposed risk tier. This page also displays a transparent breakdown of how points were assigned for each risk factor, offering insight into the risk drivers and the logic behind the assessment, directly referencing the SR 11-7 principles of early risk thinking and model documentation.
3.  **Narrative & Export:** Finally, the Model Owner provides a mandatory narrative explaining the assessment, potential mitigations, and any open questions. This contextual narrative is vital for comprehensive MRM. The application then compiles all registered metadata, risk assessment results, and the narrative into a single JSON artifact, which can be downloaded for integration into Apex Financial Services' broader model inventory and risk management systems, fulfilling the SR 11-7 requirement for a comprehensive set of model information.

This application ensures that Model Owners are proactively engaged in identifying and understanding potential model risks from the earliest stages, fostering a culture of responsible AI and compliance with regulatory expectations.

## 2. Code Requirements

### Import Statement

```python
from source.py import (
    RISK_SCORING_TABLE,
    TIER_THRESHOLDS,
    SCORING_VERSION,
    register_model_metadata,
    calculate_inherent_risk
)
import streamlit as st
import pandas as pd
import json
import uuid
import datetime
```

### UI Interactions and Function Invocation

The Streamlit app will invoke functions from `source.py` at specific points in the user flow:

*   **Page: Model Registration (`st.form("registration_form")`)**
    *   When the `st.form_submit_button("Register Model & Assess Risk")` is clicked:
        *   `register_model_metadata(model_details: dict)`: Invoked with all user inputs from the form.
            *   Expected outcome: A dictionary containing the full model record including `model_id`, `created_at`, `created_by`, `lab_version`.
        *   `calculate_inherent_risk(model_metadata: dict, scoring_table: dict, tier_thresholds: dict, scoring_version: str)`: Invoked with the output of `register_model_metadata`, `RISK_SCORING_TABLE`, `TIER_THRESHOLDS`, and `SCORING_VERSION` (all imported from `source.py`).
            *   Expected outcome: A dictionary containing `inherent_risk_score`, `proposed_risk_tier`, `proposed_tier_description`, `score_breakdown`, `scoring_version`. These will be merged into the `model_details` in session state.

*   **Page: Narrative & Export (`st.download_button`)**
    *   The `st.download_button` will use a JSON string generated from a consolidated dictionary of `st.session_state['model_details']` (which includes inputs, audit fields, and risk assessment results), `st.session_state['owner_risk_narrative']`, `st.session_state['mitigations_proposed']`, and `st.session_state['open_questions']`.

### `st.session_state` Design

`st.session_state` is used to preserve user inputs, computed values, and narrative across page navigations.

**Initialization (at the start of `app.py`):**

```python
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = '1) Model Registration'
if 'model_registered' not in st.session_state:
    st.session_state['model_registered'] = False
if 'model_details' not in st.session_state:
    st.session_state['model_details'] = {} # Stores all registration inputs and audit fields
if 'owner_risk_narrative' not in st.session_state:
    st.session_state['owner_risk_narrative'] = ""
if 'mitigations_proposed' not in st.session_state:
    st.session_state['mitigations_proposed'] = ""
if 'open_questions' not in st.session_state:
    st.session_state['open_questions'] = ""
if 'export_artifact' not in st.session_state:
    st.session_state['export_artifact'] = {}
```

**Update points:**

*   **Page: Model Registration**
    *   Upon successful submission of `st.form("registration_form")`:
        *   `st.session_state['model_details']` is updated with the result from `register_model_metadata`.
        *   `st.session_state['model_details']` is then updated with the results from `calculate_inherent_risk`.
        *   `st.session_state['model_registered']` is set to `True`.
        *   `st.session_state['current_page']` is automatically set to `'2) Risk Score Preview'` to guide the user.

*   **Page: Narrative & Export**
    *   Whenever `st.text_area` for `owner_risk_narrative`, `mitigations_proposed`, or `open_questions` changes:
        *   `st.session_state['owner_risk_narrative']` is updated with the current value.
        *   `st.session_state['mitigations_proposed']` is updated with the current value.
        *   `st.session_state['open_questions']` is updated with the current value.
    *   Before rendering the `st.json` preview and `st.download_button`:
        *   `st.session_state['export_artifact']` is constructed by combining `st.session_state['model_details']`, `st.session_state['owner_risk_narrative']`, `st.session_state['mitigations_proposed']`, and `st.session_state['open_questions']`.

**Read points:**

*   **Sidebar navigation:** `st.session_state['current_page']` is read to determine which page to render.
*   **Page: Risk Score Preview:**
    *   Reads `st.session_state['model_registered']` to check if registration occurred.
    *   Reads `st.session_state['model_details']['inherent_risk_score']` for `st.metric`.
    *   Reads `st.session_state['model_details']['proposed_risk_tier']` for `st.metric`.
    *   Reads `st.session_state['model_details']['proposed_tier_description']` for `st.metric`.
    *   Reads `st.session_state['model_details']['score_breakdown']` for `st.dataframe` and `st.bar_chart`.
*   **Page: Narrative & Export:**
    *   Reads `st.session_state['model_registered']` to ensure a model is registered before allowing narrative input/export.
    *   Reads `st.session_state['owner_risk_narrative']`, `st.session_state['mitigations_proposed']`, `st.session_state['open_questions']` to pre-populate text areas and construct the export artifact.
    *   Reads `st.session_state['export_artifact']` for `st.json` display and `st.download_button` data.

### Streamlit Application Markdown and Layout

The application will use a wide layout. Navigation is via a sidebar selectbox.

```python
st.set_page_config(layout="wide", page_title="AI Model Risk Self-Assessment (Lab 1)")

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"## Navigation")
    st.session_state['current_page'] = st.selectbox(
        "Choose a page",
        ["1) Model Registration", "2) Risk Score Preview", "3) Narrative & Export"],
        index=["1) Model Registration", "2) Risk Score Preview", "3) Narrative & Export"].index(st.session_state['current_page'])
    )

# --- Page: 1) Model Registration ---
if st.session_state['current_page'] == '1) Model Registration':
    st.markdown(f"# 📊 AI Model Registration & Initial Risk Assessment")
    st.markdown(f"---")
    st.markdown(f"As a **System / Model Owner** at Apex Financial Services, your role is crucial in ensuring the responsible and compliant deployment of AI models. Today, you are tasked with registering a new AI model (e.g., a Predictive Maintenance Model) into the enterprise model inventory. This is not just a bureaucratic step; it's a fundamental part of our Model Risk Management (MRM) framework, directly addressing the principles outlined in **SR Letter 11-7**.")
    st.markdown(f"")
    st.markdown(f"SR 11-7 emphasizes the importance of robust model development, implementation, and use, as well as comprehensive governance, policies, and controls. Specifically, Section IV (\"Model Development, Implementation, and Use\") highlights the need for disciplined processes, while Section VI (\"Governance, Policies, and Controls\") mandates maintaining a \"comprehensive set of information for models implemented for use\" (Page 20). Your initial model registration and self-assessment are the first line of defense, ensuring that potential model risks are identified and understood from the earliest stages of the model lifecycle. This proactive engagement helps us embed risk considerations at the source, saving time and reducing rework later, and fostering a culture of responsible AI.")
    st.markdown(f"")
    st.markdown(f"This page guides you through a simulated model registration interface, allowing you to input essential model metadata and then perform an initial, conceptual self-assessment of the model's inherent risk.")
    st.markdown(f"")
    st.markdown(f"---")
    st.markdown(f"### **SR 11-7 Key Principles Addressed:**")
    st.markdown(f"- **Model Documentation:** Capturing comprehensive metadata about the model is essential for transparency and auditability (SR 11-7, Page 21).")
    st.markdown(f"- **Early Risk Thinking:** Identifying and assessing inherent risk characteristics at the registration stage ensures proactive management of potential adverse consequences (SR 11-7, Page 3).")
    st.markdown(f"- **Model Inventory:** Contributing to the firm-wide inventory of models by providing structured information about new models (SR 11-7, Page 20).")
    st.markdown(f"- **Owner Responsibilities:** As a Model Owner, you are accountable for providing accurate information and an initial risk assessment (SR 11-7, Page 18).")
    st.markdown(f"---")

    st.markdown(f"## 1. Register Your AI Model: Metadata Input")
    st.markdown(f"As the Model Owner, your first task is to input the comprehensive metadata for your model. This detailed documentation is critical, as highlighted in SR 11-7 Section VI (\"Governance, Policies, and Controls\") and specifically regarding \"Model Inventory\" (Page 20), which states, \"Without adequate documentation, model risk assessment and management will be ineffective.\" This initial data forms the foundation for all subsequent MRM activities, ensuring clarity on the model's purpose, scope, and technical characteristics.")
    st.markdown(f"")
    st.markdown(f"Please define your model's attributes below. Pay close attention to the controlled vocabularies for risk factors (marked with '⚡'), as these will directly influence the inherent risk score.")
    st.markdown(f"")

    with st.form("registration_form"):
        st.markdown(f"### Model Core Details")
        col1, col2 = st.columns(2)
        with col1:
            model_name = st.text_input("Model Name (e.g., Predictive Maintenance Model v2.1)*", value=st.session_state['model_details'].get('model_name', ''))
            domain = st.selectbox("Domain*", options=['Operations Efficiency', 'Credit Risk', 'Market Risk', 'Fraud Detection', 'Customer Segmentation', 'Compliance', 'Other'], index=([
                'Operations Efficiency', 'Credit Risk', 'Market Risk', 'Fraud Detection', 'Customer Segmentation', 'Compliance', 'Other'
            ].index(st.session_state['model_details'].get('domain'))) if st.session_state['model_details'].get('domain') else 0)
            model_type = st.selectbox("Model Type*", options=['ML classifier (time-series)', 'Regression', 'Decision Tree', 'Neural Network', 'Statistical (e.g., ARIMA)', 'Expert Rule-based', 'Other'], index=([
                'ML classifier (time-series)', 'Regression', 'Decision Tree', 'Neural Network', 'Statistical (e.g., ARIMA)', 'Expert Rule-based', 'Other'
            ].index(st.session_state['model_details'].get('model_type'))) if st.session_state['model_details'].get('model_type') else 0)
            deployment_mode = st.selectbox("Deployment Mode*", options=['Real-time', 'Batch', 'Offline Analysis'], index=([
                'Real-time', 'Batch', 'Offline Analysis'
            ].index(st.session_state['model_details'].get('deployment_mode'))) if st.session_state['model_details'].get('deployment_mode') else 0)
            owner_team = st.text_input("Owner Team (Optional)", value=st.session_state['model_details'].get('owner_team', ''))
        with col2:
            business_use = st.text_area("Business Use & Objective*", height=150, value=st.session_state['model_details'].get('business_use', ''))
            model_stage = st.selectbox("Model Stage (Optional)", options=['Proof of Concept', 'Development', 'Pre-Production', 'Production', 'Retired'], index=([
                'Proof of Concept', 'Development', 'Pre-Production', 'Production', 'Retired'
            ].index(st.session_state['model_details'].get('model_stage'))) if st.session_state['model_details'].get('model_stage') else 0)
            deployment_region = st.text_input("Deployment Region (Optional)", value=st.session_state['model_details'].get('deployment_region', ''))

        st.markdown(f"### Inherent Risk Factors ⚡")
        st.markdown(f"Please select the characteristics that best describe your model's inherent risk profile. These selections directly feed into the risk scoring engine.")
        col3, col4 = st.columns(2)
        with col3:
            decision_criticality = st.selectbox("Decision Criticality*", options=list(RISK_SCORING_TABLE['decision_criticality'].keys()), index=(list(RISK_SCORING_TABLE['decision_criticality'].keys()).index(st.session_state['model_details'].get('decision_criticality'))) if st.session_state['model_details'].get('decision_criticality') else 0)
            data_sensitivity = st.selectbox("Data Sensitivity*", options=list(RISK_SCORING_TABLE['data_sensitivity'].keys()), index=(list(RISK_SCORING_TABLE['data_sensitivity'].keys()).index(st.session_state['model_details'].get('data_sensitivity'))) if st.session_state['model_details'].get('data_sensitivity') else 0)
        with col4:
            automation_level = st.selectbox("Automation Level*", options=list(RISK_SCORING_TABLE['automation_level'].keys()), index=(list(RISK_SCORING_TABLE['automation_level'].keys()).index(st.session_state['model_details'].get('automation_level'))) if st.session_state['model_details'].get('automation_level') else 0)
            regulatory_materiality = st.selectbox("Regulatory Materiality*", options=list(RISK_SCORING_TABLE['regulatory_materiality'].keys()), index=(list(RISK_SCORING_TABLE['regulatory_materiality'].keys()).index(st.session_state['model_details'].get('regulatory_materiality'))) if st.session_state['model_details'].get('regulatory_materiality') else 0)

        submitted = st.form_submit_button("Register Model & Assess Risk")

        if submitted:
            required_fields_check = {
                'model_name': model_name,
                'business_use': business_use,
                'domain': domain,
                'model_type': model_type,
                'decision_criticality': decision_criticality,
                'data_sensitivity': data_sensitivity,
                'automation_level': automation_level,
                'regulatory_materiality': regulatory_materiality,
                'deployment_mode': deployment_mode
            }

            missing_fields = [field for field, value in required_fields_check.items() if not value]

            if missing_fields:
                st.error(f"Please fill in all required fields (marked with '*'). Missing: {', '.join(missing_fields)}")
            else:
                raw_model_details = {
                    'model_name': model_name,
                    'business_use': business_use,
                    'domain': domain,
                    'model_type': model_type,
                    'decision_criticality': decision_criticality,
                    'data_sensitivity': data_sensitivity,
                    'automation_level': automation_level,
                    'deployment_mode': deployment_mode,
                    'regulatory_materiality': regulatory_materiality,
                    'owner_team': owner_team if owner_team else None,
                    'model_stage': model_stage if model_stage else None,
                    'deployment_region': deployment_region if deployment_region else None,
                    'model_id': st.session_state['model_details'].get('model_id') # Preserve ID if already generated
                }

                try:
                    registered_model_output = register_model_metadata(raw_model_details)
                    risk_assessment_output = calculate_inherent_risk(
                        registered_model_output, RISK_SCORING_TABLE, TIER_THRESHOLDS, SCORING_VERSION
                    )
                    st.session_state['model_details'] = {**registered_model_output, **risk_assessment_output}
                    st.session_state['model_registered'] = True
                    st.success("Model registered and risk assessed successfully! Proceed to 'Risk Score Preview'.")
                    st.session_state['current_page'] = '2) Risk Score Preview'
                    st.rerun() # Rerun to switch page immediately
                except ValueError as e:
                    st.error(f"Error during registration or assessment: {e}")

# --- Page: 2) Risk Score Preview ---
elif st.session_state['current_page'] == '2) Risk Score Preview':
    st.markdown(f"# 🔍 Inherent Risk Score Preview")
    st.markdown(f"---")
    st.markdown(f"With the model metadata captured, the next step is to perform the initial inherent risk self-assessment. This involves applying the predefined scoring logic to the model's characteristics (e.g., `decision_criticality`, `data_sensitivity`). This step allows you to \"assess the magnitude\" of model risk, a core activity in model risk management according to SR 11-7 (Page 4). Understanding the inherent risk helps in determining the appropriate level of scrutiny and governance required for the model.")
    st.markdown(f"")
    st.markdown(f"Apex Financial Services uses a rule-based system to calculate an initial inherent risk score and assign a preliminary risk tier. This system considers several key factors defined by SR 11-7 and internal policies, helping us quantify the \"magnitude\" of model risk based on factors like \"model complexity, higher uncertainty about inputs and assumptions, broader use, and larger potential impact\" (SR 11-7, Page 4).")
    st.markdown(f"---")
    
    if not st.session_state['model_registered']:
        st.warning("Please complete the 'Model Registration' page first to see the risk score preview.")
    else:
        st.markdown(f"## 2. Your Model's Inherent Risk Assessment Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Inherent Risk Score", value=st.session_state['model_details'].get('inherent_risk_score'))
        with col2:
            st.metric("Proposed Risk Tier", value=f"{st.session_state['model_details'].get('proposed_risk_tier')} - {st.session_state['model_details'].get('proposed_tier_description', '')}")

        st.markdown(f"---")
        st.markdown(f"### Scoring Methodology")
        st.markdown(f"Our framework assigns points to specific categorical values for each risk factor. The total inherent risk score is then calculated as the sum of points from each factor.")
        st.markdown(r"$$ S_{total} = \sum_{f \in \text{Factors}} P(V_f) $$")
        st.markdown(r"where $S_{total}$ is the total inherent risk score, $f$ represents a risk factor (e.g., decision criticality), and $P(V_f)$ is the points assigned to the chosen value $V_f$ for that factor.")
        st.markdown(f"")
        st.markdown(f"The preliminary risk tier is determined by comparing $S_{total}$ against predefined thresholds, as shown in the table below.")

        st.markdown(f"#### Risk Factor Scoring Table (Version: `{st.session_state['model_details'].get('scoring_version', SCORING_VERSION)}`)")
        # Reformat RISK_SCORING_TABLE for better display
        scoring_df = pd.DataFrame(RISK_SCORING_TABLE).fillna('-').T
        scoring_df.index.name = 'Risk Factor'
        st.dataframe(scoring_df, use_container_width=True)

        st.markdown(f"#### Proposed Risk Tier Thresholds")
        tier_df = pd.DataFrame.from_dict(TIER_THRESHOLDS, orient='index')
        tier_df.index.name = 'Tier'
        st.dataframe(tier_df, use_container_width=True)

        st.markdown(f"---")
        st.markdown(f"### Score Breakdown by Factor")
        st.markdown(f"This table and chart illustrate how each selected model characteristic contributed to the overall inherent risk score.")

        score_breakdown_data = st.session_state['model_details'].get('score_breakdown', {})
        if score_breakdown_data:
            breakdown_df = pd.DataFrame([
                {'Factor': k, 'Value': v['value'], 'Points': v['points']}
                for k, v in score_breakdown_data.items()
            ])
            st.dataframe(breakdown_df, use_container_width=True)

            # Bar chart
            st.markdown(f"#### Points Contribution Bar Chart")
            st.bar_chart(breakdown_df.set_index('Factor')['Points'])
        else:
            st.info("No score breakdown available.")

# --- Page: 3) Narrative & Export ---
elif st.session_state['current_page'] == '3) Narrative & Export':
    st.markdown(f"# ✍️ Narrative & Export Model Registration")
    st.markdown(f"---")
    st.markdown(f"As a Model Owner, providing a clear narrative for your model's risk assessment is a critical component of effective Model Risk Management. This narrative provides context, explains assumptions, outlines potential mitigations, and raises any open questions, enriching the structured data for future review and oversight.")
    st.markdown(f"")
    st.markdown(f"SR 11-7 Section VI (\"Governance, Policies, and Controls\") emphasizes comprehensive model documentation, stating it should be \"sufficiently detailed so that parties unfamiliar with a model can understand how the model operates, its limitations, and its key assumptions.\" Your narrative plays a key role in fulfilling this requirement by adding qualitative depth to the quantitative assessment.")
    st.markdown(f"---")

    if not st.session_state['model_registered']:
        st.warning("Please complete the 'Model Registration' page first.")
    else:
        st.markdown(f"## 3. Risk Narrative & Additional Context")
        owner_risk_narrative = st.text_area(
            "Owner's Inherent Risk Narrative (Required, Min 50 characters)*",
            value=st.session_state['owner_risk_narrative'],
            height=200,
            key="owner_risk_narrative_input"
        )
        mitigations_proposed = st.text_area(
            "Proposed Mitigations (Optional)",
            value=st.session_state['mitigations_proposed'],
            height=100,
            key="mitigations_proposed_input"
        )
        open_questions = st.text_area(
            "Open Questions / Follow-ups (Optional)",
            value=st.session_state['open_questions'],
            height=100,
            key="open_questions_input"
        )

        # Update session state with current text area values
        st.session_state['owner_risk_narrative'] = owner_risk_narrative
        st.session_state['mitigations_proposed'] = mitigations_proposed
        st.session_state['open_questions'] = open_questions

        narrative_min_length = 50
        is_narrative_valid = len(owner_risk_narrative) >= narrative_min_length
        if not is_narrative_valid:
            st.warning(f"Owner's Inherent Risk Narrative must be at least {narrative_min_length} characters long.")

        st.markdown(f"---")
        st.markdown(f"## 4. Export Model Registration Artifact")
        st.markdown(f"This section allows you to preview and export the complete model registration record, including all metadata, the inherent risk assessment, and your narrative, as a single JSON file. This artifact is ready for ingestion into Apex Financial Services' centralized model inventory.")

        # Consolidate all data for export
        export_data = {
            **st.session_state['model_details'],
            'owner_risk_narrative': st.session_state['owner_risk_narrative'],
            'mitigations_proposed': st.session_state['mitigations_proposed'] if st.session_state['mitigations_proposed'] else None,
            'open_questions': st.session_state['open_questions'] if st.session_state['open_questions'] else None,
            'export_format_version': 'lab1_export_v1'
        }
        st.session_state['export_artifact'] = export_data

        st.markdown(f"### JSON Export Preview")
        st.json(st.session_state['export_artifact'])

        # Create a downloadable JSON file
        json_output = json.dumps(st.session_state['export_artifact'], indent=4)
        download_filename = f"lab1_{st.session_state['model_details'].get('model_name', 'model_registration').replace(' ', '_').lower()}.json"

        download_button_disabled = not st.session_state['model_registered'] or not is_narrative_valid

        st.download_button(
            label="Download Model Registration JSON",
            data=json_output,
            file_name=download_filename,
            mime="application/json",
            disabled=download_button_disabled,
            help="Download button is enabled once model is registered and narrative meets minimum length."
        )

        if download_button_disabled:
            st.info("Please register a model and provide a valid narrative to enable download.")
```
