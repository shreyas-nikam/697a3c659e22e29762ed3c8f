import streamlit as st
import pandas as pd
import json
import uuid
import datetime
from source import (
    REQUIRED_FIELDS,
    RISK_SCORING_TABLE,
    TIER_THRESHOLDS,
    SCORING_VERSION,
    DOMAIN_OPTIONS,
    MODEL_TYPE_OPTIONS,
    DEPLOYMENT_MODE_OPTIONS,
    assess_model_risk,
)

st.set_page_config(
    page_title="QuLab: First Line - Model Owner's Initial Model Registration & Self-Assessment", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: First Line - Model Owner's Initial Model Registration & Self-Assessment")
st.divider()


def render_model_risk_report(data):
    """
    Renders a Model Risk Assessment report from a JSON dictionary 
    using native Streamlit components. No raw JSON is displayed.
    """

    # --- Header Section ---
    st.title(data.get("model_name", "Unknown Model"))

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.caption(f"**Model ID:** {data.get('model_id')}")
    with c2:
        st.caption(f"**Created By:** {data.get('created_by')}")
    with c3:
        st.caption(f"**Created At:** {data.get('created_at')}")

    st.markdown("---")

    # --- Risk Summary (Key Metrics) ---
    st.subheader("Risk Assessment Outcome")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Inherent Risk Score",
                  value=data.get("inherent_risk_score"))
    with m2:
        st.metric(label="Proposed Risk Tier",
                  value=data.get("proposed_risk_tier"))
    with m3:
        st.metric(label="Lab Version", value=data.get("lab_version"))
    with m4:
        st.metric(label="Model Stage", value=data.get("model_stage"))

    st.info(
        f"**Tier Description:** {data.get('proposed_tier_description')}", icon=None)

    # --- Score Breakdown ---
    st.subheader("Score Breakdown")

    breakdown_data = data.get("score_breakdown", {})
    if breakdown_data:
        breakdown_items = []
        for category, details in breakdown_data.items():
            breakdown_items.append({
                "Category": category.replace("_", " ").title(),
                "Selected Value": details.get("value"),
                "Risk Points": details.get("points")
            })

        df_breakdown = pd.DataFrame(breakdown_items)
        st.dataframe(
            df_breakdown,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Risk Points": st.column_config.NumberColumn(format="%d")
            }
        )

    # --- Model Metadata Grid ---
    st.subheader("Model Information")

    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.markdown(f"**Domain**\n\n{data.get('domain')}")
        st.markdown(
            f"**Decision Criticality**\n\n{data.get('decision_criticality')}")

    with row1_col2:
        st.markdown(f"**Model Type**\n\n{data.get('model_type')}")
        st.markdown(f"**Data Sensitivity**\n\n{data.get('data_sensitivity')}")

    with row1_col3:
        st.markdown(f"**Deployment Mode**\n\n{data.get('deployment_mode')}")
        st.markdown(f"**Automation Level**\n\n{data.get('automation_level')}")

    st.markdown(f"**Business Use Case**")
    st.markdown(f"> {data.get('business_use')}")

    # --- Narratives & Questions ---
    st.divider()

    n1, n2 = st.columns(2)
    with n1:
        st.markdown("**Owner Risk Narrative**")
        st.text_area("Narrative", value=data.get("owner_risk_narrative"),
                     height=150, disabled=True, label_visibility="collapsed")

    with n2:
        st.markdown("**Mitigations Proposed**")
        st.text_area("Mitigations", value=data.get("mitigations_proposed"),
                     height=150, disabled=True, label_visibility="collapsed")

    st.markdown("**Open Questions / Unresolved Items**")
    st.warning(data.get("open_questions"), icon=None)

    # --- Configuration (Collapsible) ---
    with st.expander("View Risk Scoring Logic & Thresholds"):
        config = data.get("scoring_config", {})

        # 1. Tier Thresholds Table
        st.markdown("#### Tier Thresholds")
        thresholds = config.get("tier_thresholds", {})
        if thresholds:
            t_data = []
            for tier, details in thresholds.items():
                t_data.append({
                    "Tier": tier,
                    "Min Score": details.get("min_score"),
                    "Description": details.get("description")
                })
            st.dataframe(pd.DataFrame(t_data), hide_index=True,
                         use_container_width=True)

        # 2. Scoring Matrix (Converted from JSON to Tables)
        st.markdown("#### Scoring Reference Matrix")
        scoring_table = config.get("risk_scoring_table", {})

        # Create 2 columns to display the scoring logic side-by-side
        cols = st.columns(2)
        idx = 0

        for category, scores in scoring_table.items():
            # Determine which column to place this table in
            with cols[idx % 2]:
                st.markdown(f"**{category.replace('_', ' ').title()}**")

                # Convert dict {Level: Score} to DataFrame
                score_df = pd.DataFrame(
                    list(scores.items()), columns=["Level", "Points"])
                st.dataframe(
                    score_df,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "Points": st.column_config.NumberColumn(format="%d")
                    }
                )
            idx += 1


# --- Session State Initialization ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = '1) Model Registration'
if 'model_registered' not in st.session_state:
    st.session_state['model_registered'] = False
if 'model_details' not in st.session_state:
    # Stores all registration inputs and audit fields
    st.session_state['model_details'] = {}
if 'owner_risk_narrative' not in st.session_state:
    st.session_state['owner_risk_narrative'] = ""
if "owner_risk_narrative_input" not in st.session_state:
    st.session_state["owner_risk_narrative_input"] = ""
if 'mitigations_proposed' not in st.session_state:
    st.session_state['mitigations_proposed'] = ""
if 'open_questions' not in st.session_state:
    st.session_state['open_questions'] = ""
if 'export_artifact' not in st.session_state:
    st.session_state['export_artifact'] = {}

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown(f"## Navigation")
    page_options = ["1) Model Registration",
                    "2) Risk Score Preview", "3) Narrative & Export"]

    # Determine index safely
    try:
        current_index = page_options.index(st.session_state['current_page'])
    except ValueError:
        current_index = 0

    st.session_state['current_page'] = st.selectbox(
        "Choose a page",
        page_options,
        index=current_index
    )

# --- Page: 1) Model Registration ---
if st.session_state['current_page'] == '1) Model Registration':
    st.markdown(f"As a **System / Model Owner** at Apex Financial Services, your role is crucial in ensuring the responsible and compliant deployment of AI models. Today, you are tasked with registering a new AI model (e.g., a Predictive Maintenance Model) into the enterprise model inventory. This is not just a bureaucratic step; it's a fundamental part of our Model Risk Management (MRM) framework, directly addressing the principles outlined in **SR Letter 11-7**.")
    st.markdown(f"")
    st.markdown(f"SR 11-7 emphasizes the importance of robust model development, implementation, and use, as well as comprehensive governance, policies, and controls. Specifically, Section IV (\"Model Development, Implementation, and Use\") highlights the need for disciplined processes, while Section VI (\"Governance, Policies, and Controls\") mandates maintaining a \"comprehensive set of information for models implemented for use\". Your initial model registration and self-assessment are the first line of defense, ensuring that potential model risks are identified and understood from the earliest stages of the model lifecycle. This proactive engagement helps us embed risk considerations at the source, saving time and reducing rework later, and fostering a culture of responsible AI.")
    st.markdown(f"")
    st.markdown(f"This page guides you through a simulated model registration interface, allowing you to input essential model metadata and then perform an initial, conceptual self-assessment of the model's inherent risk.")
    st.markdown(f"")
    st.markdown(f"---")
    st.markdown(f"### **SR 11-7 Key Principles Addressed:**")
    st.markdown(f"- **Model Documentation:** Capturing comprehensive metadata about the model is essential for transparency and auditability.")
    st.markdown(f"- **Early Risk Thinking:** Identifying and assessing inherent risk characteristics at the registration stage ensures proactive management of potential adverse consequences.")
    st.markdown(f"- **Model Inventory:** Contributing to the firm-wide inventory of models by providing structured information about new models.")
    st.markdown(f"- **Owner Responsibilities:** As a Model Owner, you are accountable for providing accurate information and an initial risk assessment.")
    st.markdown(f"---")

    st.markdown(f"## 1. Register Your AI Model: Metadata Input")
    st.markdown(f"As the Model Owner, your first task is to input the comprehensive metadata for your model. This detailed documentation is critical, as highlighted in SR 11-7 Section VI (\"Governance, Policies, and Controls\") and specifically regarding \"Model Inventory\", which states, \"Without adequate documentation, model risk assessment and management will be ineffective.\" This initial data forms the foundation for all subsequent MRM activities, ensuring clarity on the model's purpose, scope, and technical characteristics.")
    st.markdown(f"")
    st.markdown(f"Please define your model's attributes below. Pay close attention to the controlled vocabularies for risk factors (marked with '⚡'), as these will directly influence the inherent risk score.")
    st.markdown(f"")

    t1, t2 = st.tabs(["Model Registration Form", "Import from JSON"])
    with t1:

        with st.form("registration_form"):
            st.markdown(f"### Model Core Details")
            col1, col2 = st.columns(2)
            with col1:
                model_name = st.text_input("Model Name (e.g., Predictive Maintenance Model v2.1)*",
                                           value=st.session_state['model_details'].get('model_name', ''))

                domain_opts = DOMAIN_OPTIONS
                domain_idx = domain_opts.index(st.session_state['model_details'].get(
                    'domain')) if st.session_state['model_details'].get('domain') in domain_opts else 0
                domain = st.selectbox(
                    "Domain*", options=domain_opts, index=domain_idx)

                type_opts = MODEL_TYPE_OPTIONS
                type_idx = type_opts.index(st.session_state['model_details'].get(
                    'model_type')) if st.session_state['model_details'].get('model_type') in type_opts else 0
                model_type = st.selectbox(
                    "Model Type*", options=type_opts, index=type_idx)

                dep_opts = DEPLOYMENT_MODE_OPTIONS
                dep_idx = dep_opts.index(st.session_state['model_details'].get(
                    'deployment_mode')) if st.session_state['model_details'].get('deployment_mode') in dep_opts else 0
                deployment_mode = st.selectbox(
                    "Deployment Mode*", options=dep_opts, index=dep_idx)

                owner_team = st.text_input(
                    "Owner Team (Optional)", value=st.session_state['model_details'].get('owner_team', ''))
            with col2:
                business_use = st.text_area("Business Use & Objective*", height=150,
                                            value=st.session_state['model_details'].get('business_use', ''))

                stage_opts = ['Proof of Concept', 'Development',
                              'Pre-Production', 'Production', 'Retired']
                stage_idx = stage_opts.index(st.session_state['model_details'].get(
                    'model_stage')) if st.session_state['model_details'].get('model_stage') in stage_opts else 0
                model_stage = st.selectbox(
                    "Model Stage (Optional)", options=stage_opts, index=stage_idx)

                deployment_region = st.text_input(
                    "Deployment Region (Optional)", value=st.session_state['model_details'].get('deployment_region', ''))

            st.markdown(f"### Inherent Risk Factors ⚡")
            st.markdown(f"Please select the characteristics that best describe your model's inherent risk profile. These selections directly feed into the risk scoring engine.")
            col3, col4 = st.columns(2)

            # Helper to get safe index
            def get_idx(options, key):
                val = st.session_state['model_details'].get(key)
                return list(options).index(val) if val in options else 0

            with col3:
                crit_opts = list(
                    RISK_SCORING_TABLE['decision_criticality'].keys())
                decision_criticality = st.selectbox(
                    "Decision Criticality*", options=crit_opts, index=get_idx(crit_opts, 'decision_criticality'))

                sens_opts = list(RISK_SCORING_TABLE['data_sensitivity'].keys())
                data_sensitivity = st.selectbox(
                    "Data Sensitivity*", options=sens_opts, index=get_idx(sens_opts, 'data_sensitivity'))
            with col4:
                auto_opts = list(RISK_SCORING_TABLE['automation_level'].keys())
                automation_level = st.selectbox(
                    "Automation Level*", options=auto_opts, index=get_idx(auto_opts, 'automation_level'))

                reg_opts = list(
                    RISK_SCORING_TABLE['regulatory_materiality'].keys())
                regulatory_materiality = st.selectbox(
                    "Regulatory Materiality*", options=reg_opts, index=get_idx(reg_opts, 'regulatory_materiality'))

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

                missing_fields = [field for field,
                                  value in required_fields_check.items() if not value]

                if missing_fields:
                    st.error(
                        f"Please fill in all required fields (marked with '*'). Missing: {', '.join(missing_fields)}")
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
                        # Preserve ID if already generated
                        'model_id': st.session_state['model_details'].get('model_id')
                    }

                    try:
                        final_model_record = assess_model_risk(
                            raw_model_details)
                        st.session_state["model_details"] = final_model_record
                        st.session_state['model_registered'] = True
                        st.success(
                            "Model registered and risk assessed successfully! Proceed to 'Risk Score Preview'.")
                        st.session_state['current_page'] = '2) Risk Score Preview'
                        st.rerun()  # Rerun to switch page immediately
                    except ValueError as e:
                        st.error(f"Validation error: {e}")
                        st.info(
                            f"Required fields: {', '.join(REQUIRED_FIELDS)}")

    with t2:
        uploaded_artifact = st.file_uploader(
            "Upload a Lab 1 exported JSON to resume/edit",
            type=["json"],
            key="import_uploader"
        )

        def _safe_get(dct, key, default=None):
            return dct.get(key, default) if isinstance(dct, dict) else default

        if uploaded_artifact is not None:
            try:
                imported = json.load(uploaded_artifact)

                # --- Minimal validation (keep strict enough to avoid junk) ---
                if _safe_get(imported, "export_format_version") != "lab1_export_v1":
                    st.error(
                        "This doesn't look like a Lab 1 export (export_format_version mismatch).")
                elif not _safe_get(imported, "model_id") or not _safe_get(imported, "model_name"):
                    st.error("Invalid artifact: missing model_id/model_name.")
                else:
                    # Load into session for form pre-fill + downstream pages
                    st.session_state["model_details"] = imported
                    st.session_state["model_registered"] = True

                    # Load narrative fields too (so Page 3 is prefilled)
                    st.session_state["owner_risk_narrative"] = _safe_get(
                        imported, "owner_risk_narrative", "") or ""
                    st.session_state["mitigations_proposed"] = _safe_get(
                        imported, "mitigations_proposed", "") or ""
                    st.session_state["open_questions"] = _safe_get(
                        imported, "open_questions", "") or ""

                    st.success(
                        f"Loaded: {imported['model_name']} (ID: {imported['model_id']})")

                    # Optional: jump user to preview immediately
                    if st.button("Go to Risk Score Preview"):
                        st.session_state["current_page"] = "2) Risk Score Preview"
                        st.rerun()

            except Exception as e:
                st.error(f"Could not read JSON: {e}")
# --- Page: 2) Risk Score Preview ---
elif st.session_state['current_page'] == '2) Risk Score Preview':
    st.markdown(f"With the model metadata captured, the next step is to perform the initial inherent risk self-assessment. This involves applying the predefined scoring logic to the model's characteristics (e.g., `decision_criticality`, `data_sensitivity`). This step allows you to \"assess the magnitude\" of model risk, a core activity in model risk management according to SR 11-7. Understanding the inherent risk helps in determining the appropriate level of scrutiny and governance required for the model.")
    st.markdown(f"")
    st.markdown(f"Apex Financial Services uses a rule-based system to calculate an initial inherent risk score and assign a preliminary risk tier. This system considers several key factors defined by SR 11-7 and internal policies, helping us quantify the \"magnitude\" of model risk based on factors like \"model complexity, higher uncertainty about inputs and assumptions, broader use, and larger potential impact\" (SR 11-7, Page 4).")
    st.markdown(f"---")

    if not st.session_state['model_registered']:
        st.warning(
            "Please complete the 'Model Registration' page first to see the risk score preview.")
    else:
        st.markdown(f"## 2. Your Model's Inherent Risk Assessment Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Inherent Risk Score", value=st.session_state['model_details'].get(
                'inherent_risk_score'))
        with col2:
            st.metric("Proposed Risk Tier",
                      value=f"{st.session_state['model_details'].get('proposed_risk_tier')} - {st.session_state['model_details'].get('proposed_tier_description', '')}")

        st.markdown(f"---")
        st.markdown(f"### Scoring Methodology")
        st.markdown(f"Our framework assigns points to specific categorical values for each risk factor. The total inherent risk score is then calculated as the sum of points from each factor.")
        st.markdown(r"""$$ 
S_{total} = \sum_{f \in \text{Factors}} P(V_f) 
$$""")
        st.markdown(r"where $S_{total}$ is the total inherent risk score, $f$ represents a risk factor (e.g., decision criticality), and $P(V_f)$ is the points assigned to the chosen value $V_f$ for that factor.")
        st.markdown(f"")
        st.markdown(
            r"The preliminary risk tier is determined by comparing $S_{total}$ against predefined thresholds, as shown in the table below.")

        st.markdown(
            f"#### Risk Factor Scoring Table (Version: `{st.session_state['model_details'].get('scoring_version', SCORING_VERSION)}`)")
        # Reformat RISK_SCORING_TABLE for better display
        rows = []
        for factor, mapping in RISK_SCORING_TABLE.items():
            for category, points in mapping.items():
                rows.append(
                    {"Risk Factor": factor, "Category": category, "Points": points})
        scoring_long_df = pd.DataFrame(rows)
        st.dataframe(scoring_long_df, width='stretch')

        st.markdown(f"#### Proposed Risk Tier Thresholds")
        tier_df = pd.DataFrame.from_dict(TIER_THRESHOLDS, orient='index')
        tier_df.index.name = 'Tier'
        st.dataframe(tier_df, width='stretch')

        st.markdown(f"---")
        st.markdown(f"### Score Breakdown by Factor")
        st.markdown(
            f"This table and chart illustrate how each selected model characteristic contributed to the overall inherent risk score.")

        score_breakdown_data = st.session_state['model_details'].get(
            'score_breakdown', {})
        if score_breakdown_data:
            breakdown_df = pd.DataFrame([
                {'Factor': k, 'Value': v['value'], 'Points': v['points']}
                for k, v in score_breakdown_data.items()
            ])
            st.dataframe(breakdown_df, width='stretch')

            # Bar chart
            st.markdown(f"#### Points Contribution Bar Chart")
            st.bar_chart(breakdown_df.set_index('Factor')['Points'])
        else:
            st.info("No score breakdown available.")

# --- Page: 3) Narrative & Export ---
elif st.session_state['current_page'] == '3) Narrative & Export':

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
            st.warning(
                f"Owner's Inherent Risk Narrative must be at least {narrative_min_length} characters long.")

        st.markdown(f"---")

        if st.button("Export Model Registration Artifact"):
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

            render_model_risk_report(st.session_state['export_artifact'])

            with st.expander("View Raw JSON"):
                json_preview = json.dumps(
                    st.session_state['export_artifact'], indent=4)
                st.code(json_preview, language='json')

            # Create a downloadable JSON file
            json_output = json.dumps(
                st.session_state['export_artifact'], indent=4)
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
                st.info(
                    "Please register a model and provide a valid narrative to enable download.")

# License
st.caption('''
---
## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
''')
