import streamlit as st
import pandas as pd
import json
import uuid
import datetime
from source import (
    RISK_SCORING_TABLE,
    TIER_THRESHOLDS,
    SCORING_VERSION,
    register_model_metadata,
    calculate_inherent_risk
)

st.set_page_config(page_title="QuLab: First Line - Model Owner's Initial Model Registration & Self-Assessment", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: First Line - Model Owner's Initial Model Registration & Self-Assessment")
st.divider()

# --- Session State Initialization ---
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

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown(f"## Navigation")
    page_options = ["1) Model Registration", "2) Risk Score Preview", "3) Narrative & Export"]
    
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
            
            domain_opts = ['Operations Efficiency', 'Credit Risk', 'Market Risk', 'Fraud Detection', 'Customer Segmentation', 'Compliance', 'Other']
            domain_idx = domain_opts.index(st.session_state['model_details'].get('domain')) if st.session_state['model_details'].get('domain') in domain_opts else 0
            domain = st.selectbox("Domain*", options=domain_opts, index=domain_idx)
            
            type_opts = ['ML classifier (time-series)', 'Regression', 'Decision Tree', 'Neural Network', 'Statistical (e.g., ARIMA)', 'Expert Rule-based', 'Other']
            type_idx = type_opts.index(st.session_state['model_details'].get('model_type')) if st.session_state['model_details'].get('model_type') in type_opts else 0
            model_type = st.selectbox("Model Type*", options=type_opts, index=type_idx)
            
            dep_opts = ['Real-time', 'Batch', 'Offline Analysis']
            dep_idx = dep_opts.index(st.session_state['model_details'].get('deployment_mode')) if st.session_state['model_details'].get('deployment_mode') in dep_opts else 0
            deployment_mode = st.selectbox("Deployment Mode*", options=dep_opts, index=dep_idx)
            
            owner_team = st.text_input("Owner Team (Optional)", value=st.session_state['model_details'].get('owner_team', ''))
        with col2:
            business_use = st.text_area("Business Use & Objective*", height=150, value=st.session_state['model_details'].get('business_use', ''))
            
            stage_opts = ['Proof of Concept', 'Development', 'Pre-Production', 'Production', 'Retired']
            stage_idx = stage_opts.index(st.session_state['model_details'].get('model_stage')) if st.session_state['model_details'].get('model_stage') in stage_opts else 0
            model_stage = st.selectbox("Model Stage (Optional)", options=stage_opts, index=stage_idx)
            
            deployment_region = st.text_input("Deployment Region (Optional)", value=st.session_state['model_details'].get('deployment_region', ''))

        st.markdown(f"### Inherent Risk Factors ⚡")
        st.markdown(f"Please select the characteristics that best describe your model's inherent risk profile. These selections directly feed into the risk scoring engine.")
        col3, col4 = st.columns(2)
        
        # Helper to get safe index
        def get_idx(options, key):
            val = st.session_state['model_details'].get(key)
            return list(options).index(val) if val in options else 0

        with col3:
            crit_opts = list(RISK_SCORING_TABLE['decision_criticality'].keys())
            decision_criticality = st.selectbox("Decision Criticality*", options=crit_opts, index=get_idx(crit_opts, 'decision_criticality'))
            
            sens_opts = list(RISK_SCORING_TABLE['data_sensitivity'].keys())
            data_sensitivity = st.selectbox("Data Sensitivity*", options=sens_opts, index=get_idx(sens_opts, 'data_sensitivity'))
        with col4:
            auto_opts = list(RISK_SCORING_TABLE['automation_level'].keys())
            automation_level = st.selectbox("Automation Level*", options=auto_opts, index=get_idx(auto_opts, 'automation_level'))
            
            reg_opts = list(RISK_SCORING_TABLE['regulatory_materiality'].keys())
            regulatory_materiality = st.selectbox("Regulatory Materiality*", options=reg_opts, index=get_idx(reg_opts, 'regulatory_materiality'))

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
