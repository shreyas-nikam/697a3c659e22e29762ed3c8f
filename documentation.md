id: 697a3c659e22e29762ed3c8f_documentation
summary: First Line - Model Owner's Initial Model Registration & Self-Assessment Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: First Line - AI Model Registration & Self-Assessment Codelab

## 1. Introduction to QuLab and Model Risk Management
Duration: 0:05

Welcome to the **QuLab: First Line - AI Model Registration & Self-Assessment** codelab! In this guide, you will explore a Streamlit application designed to facilitate the initial registration and inherent risk self-assessment of AI models. This tool is critical for organizations like Apex Financial Services in managing model risk effectively, aligning with regulatory guidance such as **SR Letter 11-7**.

<aside class="positive">
<b>SR Letter 11-7</b>, issued by the Federal Reserve and OCC, outlines comprehensive guidance on Model Risk Management (MRM). It emphasizes the importance of robust model development, implementation, use, and ongoing validation, along with strong governance, policies, and controls across the model lifecycle.
</aside>

### Why is this application important?

*   **First Line of Defense:** As a Model Owner, you are the "first line" in identifying and assessing risks associated with your models. This application empowers you to document your model and its inherent risk profile at the earliest stages.
*   **Regulatory Compliance:** It directly addresses key principles of SR 11-7, including model documentation, early risk thinking, contributing to a firm-wide model inventory, and clarifying owner responsibilities.
*   **Proactive Risk Management:** By identifying potential risks upfront, organizations can embed risk considerations from the start, reducing future rework and fostering a culture of responsible AI.
*   **Transparency and Auditability:** The structured data and narrative captured ensure that model information is clear, consistent, and auditable, which is vital for internal oversight and external regulatory reviews.

### Core Concepts Explained:

1.  **Model Inventory:** A comprehensive catalog of all models used by an institution, including their metadata, purpose, and risk profiles. This application helps build this inventory.
2.  **Inherent Risk:** The level of risk associated with a model *before* any mitigating controls are put in place. It's determined by factors like the model's complexity, impact, data sensitivity, and automation level.
3.  **Risk Tiers:** Categorizations (e.g., Low, Medium, High, Critical) based on the inherent risk score, which dictate the level of governance, validation, and oversight required for a model.
4.  **Model Owner Accountability:** The responsibility of the individual or team for the model's performance, risk assessment, and adherence to policies throughout its lifecycle.

### Application Workflow:

The Streamlit application guides you through three main pages:

1.  **Model Registration:** Input essential metadata and select inherent risk factors.
2.  **Risk Score Preview:** View the calculated inherent risk score and proposed tier based on your inputs, along with a breakdown of the scoring methodology.
3.  **Narrative & Export:** Add qualitative risk narratives, proposed mitigations, and export the complete model registration artifact as a JSON file.

By the end of this codelab, you will have a comprehensive understanding of how this application facilitates efficient and compliant AI model registration and initial risk assessment.

## 2. Setting Up Your Development Environment
Duration: 0:10

To run the Streamlit application and follow along, you'll need Python installed (preferably Python 3.8+).

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### 2.1. Create Project Directory and Install Dependencies

First, create a new directory for your project and navigate into it:

```console
mkdir qu_lab_mrm_app
cd qu_lab_mrm_app
```

Next, create a virtual environment and activate it (recommended practice):

```console
python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Now, install the necessary Python packages:

```console
pip install streamlit pandas
```

### 2.2. Create `source.py`
The application relies on helper functions defined in a `source.py` file. Create a file named `source.py` in your `qu_lab_mrm_app` directory and add the following content:

```python
# source.py
import uuid
import datetime

# Define the risk scoring table based on the application's display
RISK_SCORING_TABLE = {
    'decision_criticality': {
        'Low (Informational, No Financial Impact)': 1,
        'Medium (Operational Impact, Minor Financial)': 3,
        'High (Direct Financial/Reputational Impact)': 5,
        'Critical (Regulatory, Systemic Impact)': 7
    },
    'data_sensitivity': {
        'Public/Aggregated': 1,
        'Internal Confidential': 3,
        'Personal Identifiable Information (PII)': 5,
        'Sensitive PII (e.g., Health, Biometric)': 7
    },
    'automation_level': {
        'Manual intervention always required': 1,
        'Semi-automated (human review)': 3,
        'Fully automated (low impact)': 5,
        'Fully automated (high impact, no human review)': 7
    },
    'regulatory_materiality': {
        'Not regulated/Low impact': 1,
        'Internal policy/Minor regulatory': 3,
        'Significant regulatory/Compliance focus': 5,
        'Highly regulated/Systemic risk': 7
    }
}

# Define the tier thresholds based on the application's display
TIER_THRESHOLDS = {
    'Low': {'min_score': 0, 'max_score': 5, 'description': 'Minimal oversight required'},
    'Medium': {'min_score': 6, 'max_score': 15, 'description': 'Standard review and documentation'},
    'High': {'min_score': 16, 'max_score': 20, 'description': 'Enhanced scrutiny, independent validation'},
    'Critical': {'min_score': 21, 'max_score': 28, 'description': 'Highest level of review, board oversight'}
}

SCORING_VERSION = "1.0.0"

def register_model_metadata(model_details):
    """
    Simulates the registration of model metadata.
    Generates a unique model ID and audit timestamps.
    """
    if 'model_id' not in model_details or not model_details['model_id']:
        model_details['model_id'] = str(uuid.uuid4())
    model_details['registration_date'] = datetime.datetime.now().isoformat()
    model_details['last_updated_date'] = datetime.datetime.now().isoformat()
    model_details['scoring_version'] = SCORING_VERSION
    return model_details

def calculate_inherent_risk(model_details, risk_scoring_table, tier_thresholds, scoring_version):
    """
    Calculates the inherent risk score and assigns a proposed risk tier
    based on the provided risk factors and scoring tables.
    """
    total_score = 0
    score_breakdown = {}

    risk_factors_to_assess = [
        'decision_criticality',
        'data_sensitivity',
        'automation_level',
        'regulatory_materiality'
    ]

    for factor in risk_factors_to_assess:
        value = model_details.get(factor)
        if value and value in risk_scoring_table.get(factor, {}):
            points = risk_scoring_table[factor][value]
            total_score += points
            score_breakdown[factor] = {'value': value, 'points': points}
        else:
            raise ValueError(f"Missing or invalid value for risk factor: {factor}. Value: '{value}'")

    proposed_risk_tier = 'Unknown'
    proposed_tier_description = ''
    for tier, data in tier_thresholds.items():
        if data['min_score'] <= total_score <= data['max_score']:
            proposed_risk_tier = tier
            proposed_tier_description = data['description']
            break
    
    # Handle cases where the score might fall outside defined tiers (e.g., if thresholds don't cover all possibilities)
    if proposed_risk_tier == 'Unknown':
        # Find the highest tier if score exceeds max of all, or lowest if below min of all
        all_max_score = max(t['max_score'] for t in tier_thresholds.values())
        all_min_score = min(t['min_score'] for t in tier_thresholds.values())
        if total_score > all_max_score:
            # Assign to the highest defined tier
            proposed_risk_tier = max(tier_thresholds, key=lambda k: tier_thresholds[k]['max_score'])
            proposed_tier_description = tier_thresholds[proposed_risk_tier]['description']
        elif total_score < all_min_score:
            # Assign to the lowest defined tier
            proposed_risk_tier = min(tier_thresholds, key=lambda k: tier_thresholds[k]['min_score'])
            proposed_tier_description = tier_thresholds[proposed_risk_tier]['description']


    model_details['inherent_risk_score'] = total_score
    model_details['proposed_risk_tier'] = proposed_risk_tier
    model_details['proposed_tier_description'] = proposed_tier_description
    model_details['score_breakdown'] = score_breakdown
    return model_details
```

### 2.3. Create `app.py`
Now, create a file named `app.py` in the same directory and paste the entire Streamlit application code provided in the problem description.

```python
# app.py (copy the provided Streamlit code here)
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

#  Session State Initialization 
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

#  Sidebar Navigation 
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

#  Page: 1) Model Registration 
if st.session_state['current_page'] == '1) Model Registration':
    st.markdown(f"# 📊 AI Model Registration & Initial Risk Assessment")
    st.markdown(f"")
    st.markdown(f"As a **System / Model Owner** at Apex Financial Services, your role is crucial in ensuring the responsible and compliant deployment of AI models. Today, you are tasked with registering a new AI model (e.g., a Predictive Maintenance Model) into the enterprise model inventory. This is not just a bureaucratic step; it's a fundamental part of our Model Risk Management (MRM) framework, directly addressing the principles outlined in **SR Letter 11-7**.")
    st.markdown(f"")
    st.markdown(f"SR 11-7 emphasizes the importance of robust model development, implementation, and use, as well as comprehensive governance, policies, and controls. Specifically, Section IV (\"Model Development, Implementation, and Use\") highlights the need for disciplined processes, while Section VI (\"Governance, Policies, and Controls\") mandates maintaining a \"comprehensive set of information for models implemented for use\" (Page 20). Your initial model registration and self-assessment are the first line of defense, ensuring that potential model risks are identified and understood from the earliest stages of the model lifecycle. This proactive engagement helps us embed risk considerations at the source, saving time and reducing rework later, and fostering a culture of responsible AI.")
    st.markdown(f"")
    st.markdown(f"")
    st.markdown(f"### **SR 11-7 Key Principles Addressed:**")
    st.markdown(f"- **Model Documentation:** Capturing comprehensive metadata about the model is essential for transparency and auditability (SR 11-7, Page 21).")
    st.markdown(f"- **Early Risk Thinking:** Identifying and assessing inherent risk characteristics at the registration stage ensures proactive management of potential adverse consequences (SR 11-7, Page 3).")
    st.markdown(f"- **Model Inventory:** Contributing to the firm-wide inventory of models by providing structured information about new models (SR 11-7, Page 20).")
    st.markdown(f"- **Owner Responsibilities:** As a Model Owner, you are accountable for providing accurate information and an initial risk assessment (SR 11-7, Page 18).")
    st.markdown(f"")

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

#  Page: 2) Risk Score Preview 
elif st.session_state['current_page'] == '2) Risk Score Preview':
    st.markdown(f"# 🔍 Inherent Risk Score Preview")
    st.markdown(f"")
    st.markdown(f"With the model metadata captured, the next step is to perform the initial inherent risk self-assessment. This involves applying the predefined scoring logic to the model's characteristics (e.g., `decision_criticality`, `data_sensitivity`). This step allows you to \"assess the magnitude\" of model risk, a core activity in model risk management according to SR 11-7 (Page 4). Understanding the inherent risk helps in determining the appropriate level of scrutiny and governance required for the model.")
    st.markdown(f"")
    st.markdown(f"Apex Financial Services uses a rule-based system to calculate an initial inherent risk score and assign a preliminary risk tier. This system considers several key factors defined by SR 11-7 and internal policies, helping us quantify the \"magnitude\" of model risk based on factors like \"model complexity, higher uncertainty about inputs and assumptions, broader use, and larger potential impact\" (SR 11-7, Page 4).")
    st.markdown(f"")
    
    if not st.session_state['model_registered']:
        st.warning("Please complete the 'Model Registration' page first to see the risk score preview.")
    else:
        st.markdown(f"## 2. Your Model's Inherent Risk Assessment Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Inherent Risk Score", value=st.session_state['model_details'].get('inherent_risk_score'))
        with col2:
            st.metric("Proposed Risk Tier", value=f"{st.session_state['model_details'].get('proposed_risk_tier')} - {st.session_state['model_details'].get('proposed_tier_description', '')}")

        st.markdown(f"")
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

        st.markdown(f"")
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

#  Page: 3) Narrative & Export 
elif st.session_state['current_page'] == '3) Narrative & Export':
    st.markdown(f"# ✍️ Narrative & Export Model Registration")
    st.markdown(f"")
    st.markdown(f"As a Model Owner, providing a clear narrative for your model's risk assessment is a critical component of effective Model Risk Management. This narrative provides context, explains assumptions, outlines potential mitigations, and raises any open questions, enriching the structured data for future review and oversight.")
    st.markdown(f"")
    st.markdown(f"SR 11-7 Section VI (\"Governance, Policies, and Controls\") emphasizes comprehensive model documentation, stating it should be \"sufficiently detailed so that parties unfamiliar with a model can understand how the model operates, its limitations, and its key assumptions.\" Your narrative plays a key role in fulfilling this requirement by adding qualitative depth to the quantitative assessment.")
    st.markdown(f"")

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

        st.markdown(f"")
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

### 2.4. Run the Streamlit Application

With both `source.py` and `app.py` in the same directory, you can now run the Streamlit application from your terminal:

```console
streamlit run app.py
```

This command will open the application in your default web browser (usually at `http://localhost:8501`).

## 3. Model Registration - Inputting Core Metadata
Duration: 0:15

The first page of the application, "1) Model Registration", is where you, as the Model Owner, begin the process of documenting your AI model. This section gathers essential metadata and initial risk characteristics.

### 3.1. Overview of the Registration Page

Upon navigating to "1) Model Registration" from the sidebar, you'll see a detailed introduction emphasizing the importance of this step for SR 11-7 compliance.

The form is structured into two main sections:
*   **Model Core Details:** Basic information about the model.
*   **Inherent Risk Factors ⚡:** Key characteristics that drive the initial risk assessment.

### 3.2. Filling out Model Core Details

Let's walk through the fields in the "Model Core Details" section. Fields marked with an asterisk `*` are required.

*   **Model Name:** A unique identifier for your model (e.g., "Predictive Maintenance Model v2.1").
*   **Business Use & Objective:** A detailed description of what the model does and its business purpose. This is crucial for understanding its impact.
*   **Domain:** The business area the model operates in (e.g., 'Operations Efficiency', 'Credit Risk', 'Fraud Detection').
*   **Model Type:** The underlying methodology of the model (e.g., 'ML classifier (time-series)', 'Neural Network', 'Regression').
*   **Deployment Mode:** How the model operates in production (e.g., 'Real-time', 'Batch', 'Offline Analysis'). This can influence latency and immediate impact risks.
*   **Owner Team (Optional):** The team responsible for the model.
*   **Model Stage (Optional):** Its current phase in the lifecycle (e.g., 'Development', 'Production').
*   **Deployment Region (Optional):** Geographic deployment location.

**Example Input:**

| Field               | Example Value                         |
| : | : |
| Model Name          | Customer Churn Predictor v1.0         |
| Business Use        | Identify customers at high risk of churn to enable proactive retention strategies. |
| Domain              | Customer Segmentation                 |
| Model Type          | ML classifier (time-series)           |
| Deployment Mode     | Batch                                 |
| Owner Team          | Customer Insights                     |
| Model Stage         | Production                            |
| Deployment Region   | North America                         |

### 3.3. Selecting Inherent Risk Factors ⚡

This section is vital as your selections here directly contribute to the model's inherent risk score. Each option has a predefined point value.

*   **Decision Criticality:** The impact of the model's decisions.
    *   *Example:* For a churn predictor impacting marketing campaigns, 'High (Direct Financial/Reputational Impact)' might be appropriate.
*   **Data Sensitivity:** The type of data the model processes.
    *   *Example:* If it uses customer transaction history and demographics, 'Personal Identifiable Information (PII)' is likely.
*   **Automation Level:** The degree of human intervention in the model's output usage.
    *   *Example:* If the model's output automatically triggers marketing offers, 'Fully automated (high impact, no human review)' is relevant.
*   **Regulatory Materiality:** The level of regulatory scrutiny or compliance requirements.
    *   *Example:* Customer-facing models often fall under 'Significant regulatory/Compliance focus'.

**Example Input for Inherent Risk Factors:**

| Risk Factor            | Example Value                                        |
| : | : |
| Decision Criticality   | High (Direct Financial/Reputational Impact)          |
| Data Sensitivity       | Personal Identifiable Information (PII)              |
| Automation Level       | Fully automated (low impact)                         |
| Regulatory Materiality | Significant regulatory/Compliance focus              |

After filling out the form, click the **"Register Model & Assess Risk"** button. The application will validate the required fields and, upon successful submission, will process the data.

### 3.4. Behind the Scenes: `register_model_metadata`

When you click "Register Model & Assess Risk," the `app.py` calls the `register_model_metadata` function from `source.py`. This function is responsible for:
1.  Assigning a unique `model_id` (using `uuid.uuid4()`) if one doesn't already exist.
2.  Adding `registration_date` and `last_updated_date` timestamps.
3.  Attaching the `scoring_version` used for the assessment.

This creates a foundational record for your model within the (simulated) model inventory.

<aside class="positive">
Experiment with different selections for the Inherent Risk Factors. Notice how these choices will directly impact the total score and risk tier displayed on the next page. This interactive feedback helps Model Owners understand the drivers of model risk.
</aside>

## 4. Understanding the Inherent Risk Score Preview
Duration: 0:20

Once you've registered your model, the application automatically navigates to the "2) Risk Score Preview" page. This page presents the outcome of the inherent risk self-assessment based on the factors you selected.

### 4.1. Inherent Risk Assessment Results

At the top of the page, you'll see two key metrics:

*   **Inherent Risk Score:** This is a numerical value representing the cumulative risk of your model based on the chosen factors.
*   **Proposed Risk Tier:** A categorical assignment (e.g., 'Low', 'Medium', 'High', 'Critical') that indicates the preliminary level of oversight and governance required.

For instance, using the example inputs from the previous step:
*   Decision Criticality: High (5 points)
*   Data Sensitivity: PII (5 points)
*   Automation Level: Fully automated (low impact) (5 points)
*   Regulatory Materiality: Significant (5 points)
*   Total Score: $5 + 5 + 5 + 5 = 20$
*   Proposed Risk Tier: High

### 4.2. Scoring Methodology Explained

The application provides transparency into how the inherent risk score is calculated:

*   **Formula:** The total inherent risk score ($S_{total}$) is the sum of points ($P(V_f)$) assigned to the selected value ($V_f$) for each risk factor ($f$).
    $$ S_{total} = \sum_{f \in \text{Factors}} P(V_f) $$
    This formula is a simple additive model, which is common in initial risk assessments for its interpretability.

*   **Risk Factor Scoring Table:** This table (`RISK_SCORING_TABLE` from `source.py`) shows all possible risk factors and the points associated with each of their categorical values. This table is dynamic and its version is displayed, ensuring traceability of the scoring logic.

*   **Proposed Risk Tier Thresholds:** The `TIER_THRESHOLDS` from `source.py` defines the score ranges for each risk tier. This table demonstrates how the calculated $S_{total}$ translates into a 'Low', 'Medium', 'High', or 'Critical' tier.

The application dynamically displays these tables, allowing you to clearly see the rules governing the score.

### 4.3. Score Breakdown by Factor

To further enhance understanding, the application provides:

*   **Score Breakdown Table:** A tabular view showing each risk factor, your selected value for it, and the points it contributed to the total score. This is derived from the `score_breakdown` dictionary returned by `calculate_inherent_risk`.
*   **Points Contribution Bar Chart:** A visual representation of the breakdown, making it easy to identify which factors contribute most significantly to the overall inherent risk.

### 4.4. Behind the Scenes: `calculate_inherent_risk`

When you submitted the registration form, after `register_model_metadata`, the `app.py` called the `calculate_inherent_risk` function from `source.py`. This function:
1.  Iterates through the core risk factors (`decision_criticality`, `data_sensitivity`, `automation_level`, `regulatory_materiality`).
2.  For each factor, it looks up the points associated with the selected value in the `RISK_SCORING_TABLE`.
3.  It sums these points to get the `inherent_risk_score`.
4.  It then compares this score against the `TIER_THRESHOLDS` to determine the `proposed_risk_tier` and its description.
5.  All these results, including a `score_breakdown` dictionary, are added back to the `model_details` session state.

### Application Architecture: Data Flow for Risk Scoring

<pre>
++      +--+      ++
| Streamlit Frontend  |      |  Streamlit Session State    |      |     source.py functions   |
| (app.py)            |      |  (st.session_state)         |      |                           |
++      +--+      ++
          |                            ^                              ^         |
          | 1. User inputs model       |                              |         |
          |    metadata & risk factors |                              |         |
          V                            |                              |         |
++      +--+        |         |
| Registration Form   |-->|  'model_details' (raw)      |<-|         |
| (app.py)            |      |                             |        |         |
++      +--+        |         |
          | `submitted`        |                              |         |
          |   (Button Click)   |                              |         |
          V                    |                              |         |
    `register_model_metadata`  | 2. Adds model_id, timestamps |         |
          |                      |    and scoring_version.    |         |
          V                      |                              |         |
++      +--+        |         |
|  Updated 'model_details' |<-|                             |        |         |
| (with ID, dates)    |      |                             |        |         |
++      +--+        |         |
          |                      |                              |         |
          V                      |                              |         |
    `calculate_inherent_risk`->|  3. Uses RISK_SCORING_TABLE, |         |
          |                      |     TIER_THRESHOLDS.         |         |
          V                      |                              |         |
++      +--+        |         |
|  'model_details'    |-->|  Updated 'model_details'    |        |         |
|  (with score, tier, |      |  (inc. score_breakdown)     |        |         |
|  breakdown)         |      |                             |        |         |
++      +--+        |         |
          |                            |                              |         |
          | 4. Displays results        |                              |         |
          V                            |                              |         |
++                V                              V         V
| Risk Score Preview  |<Display--Display
| (app.py)            |
++
</pre>

<aside class="negative">
It is crucial for Model Owners to understand how their model's characteristics translate into a risk score and tier. Misclassifying a model's risk can lead to inadequate governance or, conversely, over-burdening low-risk models with excessive scrutiny.
</aside>

## 5. Adding Narrative and Exporting the Artifact
Duration: 0:10

The final page, "3) Narrative & Export", allows you to add qualitative context to your model's registration and then export the complete artifact. This narrative component is highly valued in MRM for providing insights beyond quantitative scores.

### 5.1. Providing Risk Narrative and Context

This section includes three text areas:

*   **Owner's Inherent Risk Narrative (Required):** This is a mandatory field (minimum 50 characters) where you provide a detailed qualitative assessment of the model's inherent risks. Explain *why* certain risk factors were chosen, any assumptions made, or specific concerns related to the model's operation. This fulfills the SR 11-7 requirement for comprehensive documentation.
*   **Proposed Mitigations (Optional):** Here, you can outline any initial ideas for mitigating the identified inherent risks. These might be controls already in place, or planned actions to reduce the model's risk exposure.
*   **Open Questions / Follow-ups (Optional):** Use this space to note any outstanding questions, areas requiring further investigation, or topics to be discussed with other stakeholders (e.g., model validators, risk managers).

**Example Narrative:**

> "This Customer Churn Predictor is critical due to its direct impact on marketing budget allocation and customer retention strategies. The use of PII raises data privacy concerns, necessitating robust data governance and anonymization techniques. While currently fully automated, human oversight of triggered campaigns will be crucial. Regulatory focus on customer treatment in marketing is a key consideration. Further review is needed for potential bias in feature selection against specific customer segments."

### 5.2. Exporting the Model Registration Artifact

The application consolidates all the information entered across the pages into a single JSON object.

*   **JSON Export Preview:** A live preview of the complete JSON artifact is displayed. This includes all the model metadata, the inherent risk score and tier, the score breakdown, and your narrative entries. This structured format is ideal for ingestion into a centralized model inventory system.

*   **Download Button:** The **"Download Model Registration JSON"** button allows you to download this JSON file. The button is enabled only after a model has been successfully registered and the required "Owner's Inherent Risk Narrative" meets the minimum length. The file name will be dynamically generated based on the model name.

<button>
  [Download Example JSON](data:application/json;base64,eyJtb2RlbF9uYW1lIjogIkN1c3RvbWVyIENodXJuIFByZWRpY3RvciB2MS4wIiwgImJ1c2luZXNzX3VzZSI6ICJJZGVudGlmeSBjdXN0b21lcnMgYXQgaGlnaCByaXNrIG9mIGNodXJuIHRvIGVuYWJsZSBwcm9hY3RpdmUgcmV0ZW50aW9uIHN0cmF0ZWdpZXMuIiwgImRvbWFpbiI6ICJDdXN0b21lciBTZWdtZW50YXRpb24iLCAibW9kZWxfdHlwZSI6ICJNTCBjbGFzc2lmaWVyICh0aW1lLXNlcmllcykiLCAiZGVjaXNpb25fY3JpdGljYWxpdHkiOiAiSGlnaCAoRGlyZWN0IEZpbmFuY2lhbC9SZXB1dGF0aW9uYWwgSW1wYWN0KSIsICJkYXRhX3NlbnNpdGl2aXR5IjogIlBlcnNvbmFsIElkZW50aWZpYWJsZSBJbmZvcm1hdGlvbiAoUElJKykiLCAiYXV0b21hdGlvbl9sZXZlbCI6ICJGdWxseSBhdXRvbWF0ZWQgKGxvdyBpbXBhY3QpIiwgImRlcGxveW1lbnRfbW9kZSI6ICJCYXRjaCIsICJyZWd1bGF0b3J5X21hdGVyaWFsaXR5IjogIlNpZ25pZmljYW50IHJlZ3VsYXRvcnkvQ29tcGxpYW5jZSBmb2N1cyIsICJvd25lcl90ZWFtIjogIkN1c3RvbWVyIEluc2lnaHRzIiwgIm1vZGVsX3N0YWdlIjogIlByb2R1Y3Rpb24iLCAiZGVwbG95bWVudF9yZWdpb24iOiAiTm9ydGggQW1lcmljYSIsICJtb2RlbF9pZCI6ICI5Y2IwZTkwNy1mZjIzLTQ3YjgtODgxZi02YjEzYTU3MTcyMTMiLCAicmVnaXN0cmF0aW9uX2RhdGUiOiAiMjAyMy0xMC0yNlQxMjowMDowMC4wMDAwMDAiLCAibGFzdF91cGRhdGVkX2RhdGUiOiAiMjAyMy0xMC0yNlQxMjowMDowMC4wMDAwMDAiLCAic2NvcmBpbmdfdmVyc2lvbiI6ICIxLjAuMCIsICJpbmhlcmVudF9yaXNrX3Njb3JlIjogMjAsICJwcm9wb3NlZF9yaXNrX3RpZXIiOiAiSGlnaCIsICJwcm9wb3NlZF90aWVyX2Rlc2NyaXB0aW9uIjogIkVuaGFuY2VkIHNjcnV0aW55LCBpbmRlcGVuZGVudCB2YWxpZGF0aW9uIiwgInNjb3JlX2JyZWFrZG93biI6IHsiZGVjaXNpb25fY3JpdGljYWxpdHkiOiB7InZhbHVlIjogIkhpZ2ggKERpcmVjdCBGaW5hbmNpYWwvUmVwdXRhY2lvbmFsIEltcGFjdCkiLCAicG9pbnRzIjogNX0sICJkYXRhX3NlbnNpdGl2aXR5IjogeyJ2YWx1ZSI6ICJQZXJzb25hbCBJZGVudGlmaWFibGUgSW5mb3JtYXRpb24gKFBLSSkiLCAicG9pbnRzIjogNX0sICJhdXRvbWF0aW9uX2xldmVsIjogeyJ2YWx1ZSI6ICJGdWxseSBhdXRvbWF0ZWQgKGxvdyBpbXBhY3QpIiwgInBvaW50cyI6IDV9LCAicmVndWxhdG9yeV9tYXRlcmlhbGl0eSI6IHsidmFsdWUiOiAiU2lnbmlmaWNhbnQgcmVndWxhdG9yeS9Db21wbGlhbmNlIGZvY3VzIiwgInBvaW50cyI6IDV9fSwgIm93bmVyX3Jpc2tfbmFycmF0aXZlIjogIlRoaXMgQ3VzdG9tZXIgQ2h1cm4gUHJlZGljdG9yIGlzIGNyaXRpY2FsIGR1ZSB0byBpdHMgZGlyZWN0IGltcGFjdCBvbiBtYXJrZXRpbmcgYnVkZ2V0IGFsbG9jYXRpb24gYW5kIGN1c3RvbWVyIHJldGVudGlvbiBzdHJhdGVnaWVzLiBUaGUgdXNlIG9mIFBJSSByYWlzZXMgZGF0YSBwcml2YWN5IGNvbmNlcm5zLCBuZWNlc3NpdGF0aW5nIHJvYnVzdCBkYXRhIGdvdmVybmFuY2UgYW5kIGFub255bWl6YXRpb24gdGVjaG5pcXVlcy4gV2hpbGUgY3VycmVudGx5IGZ1bGx5IGF1dG9tYXRlZCwgaHVtYW4gb3ZlcnNpZ2h0IG9mIHRyaWdnZXJlZCBjYW1wYWlnbnMgd2lsbCBiZSBjcnVjaWFsLiBSZWd1bGF0b3J5IGZvY3VzIG9uIGN1c3RvbWVyIHRyZWF0bWVudCBpbiBtYXJrZXRpbmcgaXMgYSBrZXkgY29uc2lkZXJhdGlvbi4gRnVydGhlciByZXZpZXcgaXNuZWVkZWQgZm9yIHBvdGVudGlhbCBiaWFzIGluIGZlYXR1cmUgc2VsZWN0aW9uIGFnYWluc3Qgc3BlY2lmaWMgY3VzdG9tZXIgc2VnbWVudHMuIiwgIm1pdGlnYXRpb25zX3Byb3Bvc2VkIjogIlN0cmVuZ3RoZW4gZGF0YSBlbmNyeXB0aW9uIGFuZCBhbm9ueW1pemF0aW9uLiBJbXBsZW1lbnQgbWFudWFsIHJldmlldyBzdGVwIGZvciBhbGwgdHJpZ2dlcmVkIGNhbXBhaWducy4gQ29uZHVjdCBiaWFzIGF1ZGl0cyBvbiBtb2RlbCBvdXRwdXRzLiIsICJvcGVuX3F1ZXN0aW9ucyI6ICJXYXQgaXMgdGhlIGVuZ2FnZW1lbnQgcHJvdG9jb2wgd2l0aCBSaXNrIE92ZXJzaWdodCBUZWFtPyBIb3cgZnJlT3VlbnRseSBzaG91bGQgYmlhcyByZXZpZXdzIGJlIGNvbmR1Y3RlZD8iLCAiZXhwb3J0X2Zvcm1hdF92ZXJzaW9uIjogImxhYjFfZXhwb3J0X3YxIn0=)
</button>

<aside class="positive">
The exported JSON artifact serves as a single source of truth for your model's initial registration and risk assessment. It is a critical component for integration into enterprise-wide Model Risk Management (MRM) systems and for audit trails.
</aside>

## 6. Application Architecture and Potential Enhancements
Duration: 0:10

Now that you've explored the functionalities of the application, let's briefly look at its architecture and consider how it could be extended.

### 6.1. Conceptual Architecture

The application employs a simple client-server architecture, typical for Streamlit applications:

*   **Streamlit Frontend (`app.py`):** This is the user interface layer, handling user inputs, displaying information, and managing page navigation. Streamlit's reactive nature ensures that UI components update automatically when session state or input values change.
*   **Streamlit Session State (`st.session_state`):** This is crucial for maintaining data persistence across user interactions and page navigations within a single user session. It stores `model_details`, `model_registered` status, narratives, etc.
*   **Backend Logic (`source.py`):** This module contains the core business logic, such as:
    *   **Risk Scoring Rules:** `RISK_SCORING_TABLE` and `TIER_THRESHOLDS` define the static data for risk assessment.
    *   **Model Registration Functionality:** `register_model_metadata` handles the creation of unique IDs and audit timestamps.
    *   **Risk Calculation Logic:** `calculate_inherent_risk` implements the algorithm for scoring and tiering.

<pre>
++
|            User's Browser          |
|  (Streamlit Frontend - app.py)     |
| +--+ |
| | Input Forms (Model Registration)| |
| | Risk Score Display             | |
| | Narrative & Export Interface   | |
| +--+ |
++
              ^        |
              | (HTTP/WebSocket)
              V        |
++
|       Streamlit Server (app.py)    |
| +--+ |
| |   Streamlit Session State      |< Data Persistence & Shared State
| |   ('model_details',            | |
| |    'current_page', etc.)       | |
| +-++ |
|                     |              |
|                     V              |
| +-++ |
| |  Backend Logic (source.py)     |< Business Logic & Rules
| |  - RISK_SCORING_TABLE          | |
| |  - TIER_THRESHOLDS             | |
| |  - register_model_metadata()   | |
| |  - calculate_inherent_risk()   | |
| +--+ |
++
</pre>

### 6.2. Potential Enhancements

This application provides a solid foundation, and several enhancements could further improve its capabilities and integration within an enterprise MRM framework:

1.  **Database Integration:** Instead of relying solely on Streamlit's session state and JSON file exports, integrate with a persistent database (e.g., PostgreSQL, MongoDB). This would allow for:
    *   Storing and retrieving model registrations across sessions and users.
    *   Implementing version control for model metadata and risk assessments.
    *   Enabling reporting and analytics on the entire model inventory.
2.  **User Authentication & Authorization:** Implement login capabilities to control who can register or view models, ensuring data security and compliance. Different roles (e.g., Model Owner, Validator, Risk Manager) could have different permissions.
3.  **Automated Workflow Integration:** Connect the export artifact to a broader MRM workflow system (e.g., an internal governance platform, a JIRA-like system). This could trigger validation requests, review processes, or alert relevant stakeholders.
4.  **Audit Trail and Change History:** Track all changes made to a model's registration (who, what, when) within the database, providing a comprehensive audit trail for regulatory purposes.
5.  **Dynamic Risk Scoring Models:** Allow administrators to define and update risk scoring tables and thresholds through a dedicated UI, rather than hardcoding them in `source.py`. This provides greater flexibility for evolving risk policies.
6.  **Advanced Visualizations:** Implement more sophisticated dashboards for risk managers, allowing them to visualize model risk across domains, tiers, or teams.
7.  **Integration with Model Monitoring Tools:** Link registered models to ongoing performance and explainability monitoring systems.

<aside class="positive">
By understanding the current architecture and considering these enhancements, developers can envision how this Streamlit application serves as a crucial component in a larger, more robust enterprise Model Risk Management ecosystem.
</aside>

Congratulations! You have successfully completed the QuLab: First Line - AI Model Registration & Self-Assessment Codelab. You now understand the application's functionalities, its importance in Model Risk Management, and its underlying design principles.
