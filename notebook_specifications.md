
# Model Owner's Initial Model Registration & Self-Assessment for Predictive Maintenance

**Scenario:** As **Alex Chen, a System / Model Owner** at Industrial Innovations Corp., you've been leading the development and implementation of a new "Predictive Maintenance Model." This model is designed to forecast equipment failures and optimize maintenance schedules across the company's manufacturing facilities. Before your model can go into full production, it's essential to comply with Industrial Innovations Corp.'s Model Risk Management (MRM) policies, which are heavily inspired by regulatory guidance like **SR 11-7**. Your immediate task is to register the model in the enterprise inventory and conduct a preliminary self-assessment of its inherent risk characteristics. This early documentation and risk evaluation are crucial to ensure transparency, facilitate effective challenge, and prevent downstream issues, laying the groundwork for a robust model lifecycle.

---

## 1. Setting Up the Environment and Dependencies

Before we begin the model registration process, we need to ensure our environment is set up correctly. This involves installing any necessary Python libraries and importing the modules that will help us manage data, define rules, and generate structured output.

```python
# Install required libraries (if not already installed)
!pip install pandas uuid datetime ipywidgets
```

```python
import pandas as pd
import json
import uuid
from datetime import datetime
from IPython.display import display, Markdown, HTML
import ipywidgets as widgets
from IPython.display import clear_output
```

## 2. Defining Industrial Innovations Corp.'s MRM Policy: Risk Scoring & Tiers

Alex understands that a clear, consistent policy is the backbone of effective MRM, as outlined in SR 11-7 Section VI, "Governance, Policies, and Controls." Industrial Innovations Corp. has established a deterministic scoring mechanism to assess inherent model risk. Each characteristic of a model (e.g., its criticality, data sensitivity) is assigned points, and the total score maps to a specific risk tier. This transparent approach ensures explainability and auditability for model risk decisions.

The inherent risk score, $S$, for a model is calculated as the sum of points assigned to each of its key risk drivers:

$$ S = \sum_{i=1}^{N} P_i(\text{Value}_i) $$

where $N$ is the number of risk drivers, and $P_i(\text{Value}_i)$ is the points assigned to the specific value of the $i$-th risk driver.

```python
# Define the scoring policy for inherent risk drivers
# This reflects Industrial Innovations Corp.'s internal MRM policy, aligned with SR 11-7 principles.
RISK_SCORES = {
    "decision_criticality": {
        "Low": 1,
        "Medium": 5,
        "High": 10
    },
    "data_sensitivity": {
        "Public": 0,
        "Internal": 2,
        "Confidential": 5,
        "Regulated-PII": 8
    },
    "automation_level": {
        "Advisory": 1,
        "Human-Approval": 4,
        "Fully-Automated": 7
    },
    "deployment_mode": {
        "Internal-only": 1,
        "Batch": 3,
        "Human-in-loop": 5,
        "Real-time": 8
    },
    "regulatory_materiality": {
        "None": 0,
        "Moderate": 6,
        "High": 12
    }
}

# Define the risk tier thresholds
TIER_THRESHOLDS = {
    "Tier 1": {"min_score": 22, "description": "Models with significant potential impact, requiring most stringent controls and validation."},
    "Tier 2": {"min_score": 15, "description": "Models with moderate potential impact, requiring standard controls and validation."},
    "Tier 3": {"min_score": 0, "description": "Models with limited potential impact, requiring basic controls and validation."} # Tier 3 is the lowest, acts as a fallback for scores below Tier 2
}

# Define controlled vocabularies (enums) for model metadata
CONTROLLED_VOCABULARIES = {
    "domain": ["finance", "healthcare", "engineering", "operations", "other"],
    "model_type": ["ML", "LLM", "AGENT", "Statistical"],
    "decision_criticality": ["Low", "Medium", "High"],
    "data_sensitivity": ["Public", "Internal", "Confidential", "Regulated-PII"],
    "automation_level": ["Advisory", "Human-Approval", "Fully-Automated"],
    "deployment_mode": ["Internal-only", "Batch", "Human-in-loop", "Real-time"],
    "regulatory_materiality": ["None", "Moderate", "High"]
}

# Define required fields for model registration
REQUIRED_FIELDS = [
    "model_name", "business_use", "owner", "domain", "model_type",
    "decision_criticality", "data_sensitivity", "automation_level",
    "deployment_mode", "regulatory_materiality"
]

# Define the current scoring policy version for auditability
SCORING_POLICY_VERSION = "1.0.20240310"

print("--- Industrial Innovations Corp. MRM Policy ---")
print("\nRisk Factor Scoring:")
for factor, scores in RISK_SCORES.items():
    print(f"- {factor}: {scores}")

print("\nRisk Tier Thresholds:")
for tier, details in TIER_THRESHOLDS.items():
    print(f"- {tier} (Min Score: {details['min_score']}): {details['description']}")

print(f"\nScoring Policy Version: {SCORING_POLICY_VERSION}")
```

### Explanation of Execution

These definitions form the bedrock of Industrial Innovations Corp.'s Model Risk Management framework. By explicitly defining scoring for each risk attribute and clear tier thresholds, Alex can ensure that the initial risk assessment is objective, reproducible, and transparent. This aligns with SR 11-7's emphasis on strong governance and a structured approach to identifying and managing model risk from the earliest stages.

---

## 3. Registering Core Model Metadata

Alex's first concrete step is to populate the core metadata for the Predictive Maintenance Model. This forms the entry in the enterprise model inventory, a critical requirement under SR 11-7 (Section IV, "Model Development, Implementation, and Use" and Section VI, "Model Inventory"). Comprehensive metadata ensures that the model's purpose, ownership, and basic characteristics are clearly documented for all stakeholders, fostering "effective challenge" and understanding.

```python
def get_model_metadata_ui(controlled_vocab):
    """
    Generates a UI for capturing model metadata using ipywidgets.
    Provides pre-filled values for the Predictive Maintenance Model.
    """
    
    # Pre-filled data for the Predictive Maintenance Model
    initial_data = {
        "model_id": str(uuid.uuid4()), # Generate a new UUID for each run
        "model_name": "Predictive Maintenance Model",
        "model_version": "1.0.0",
        "owner": "Alex Chen (System/Model Owner)",
        "business_use": "Predict equipment failures to optimize maintenance schedules and reduce downtime.",
        "intended_users": "Maintenance Engineers, Operations Managers",
        "model_outputs": "Probability of failure for key equipment components, recommended maintenance timing.",
        "key_assumptions": "Historical sensor data is representative of future operational conditions. Failure modes are consistent.",
        "known_limitations": "Performance may degrade with significant changes in operational environment or new equipment types. Limited data for rare failure modes.",
        "fallback_process": "Manual inspection schedules, expert judgment for fault diagnosis.",
        "third_party_dependencies": "None",
        "external_dependencies": "Sensor data streams, ERP system for maintenance records.",
        "domain": "operations", # Use lowercase as per enum
        "model_type": "ML"
    }

    # Widget definitions for core metadata
    model_name_widget = widgets.Text(description='Model Name:', value=initial_data["model_name"])
    model_version_widget = widgets.Text(description='Version:', value=initial_data["model_version"])
    owner_widget = widgets.Text(description='Owner:', value=initial_data["owner"])
    business_use_widget = widgets.Textarea(description='Business Use:', value=initial_data["business_use"], rows=3)
    domain_widget = widgets.Dropdown(description='Domain:', options=controlled_vocab["domain"], value=initial_data["domain"])
    model_type_widget = widgets.Dropdown(description='Model Type:', options=controlled_vocab["model_type"], value=initial_data["model_type"])

    # Optional but recommended fields
    intended_users_widget = widgets.Text(description='Intended Users:', value=initial_data["intended_users"])
    model_outputs_widget = widgets.Textarea(description='Model Outputs:', value=initial_data["model_outputs"], rows=2)
    key_assumptions_widget = widgets.Textarea(description='Key Assumptions:', value=initial_data["key_assumptions"], rows=2)
    known_limitations_widget = widgets.Textarea(description='Known Limitations:', value=initial_data["known_limitations"], rows=2)
    fallback_process_widget = widgets.Textarea(description='Fallback Process:', value=initial_data["fallback_process"], rows=2)
    third_party_dependencies_widget = widgets.Text(description='Third-Party Dependencies:', value=initial_data["third_party_dependencies"])
    external_dependencies_widget = widgets.Text(description='External Dependencies:', value=initial_data["external_dependencies"])
    
    # Store widgets in a dictionary for easy access
    core_widgets = {
        "model_id": widgets.Text(description='Model ID:', value=initial_data["model_id"], disabled=True),
        "model_name": model_name_widget,
        "model_version": model_version_widget,
        "owner": owner_widget,
        "business_use": business_use_widget,
        "intended_users": intended_users_widget,
        "model_outputs": model_outputs_widget,
        "key_assumptions": key_assumptions_widget,
        "known_limitations": known_limitations_widget,
        "fallback_process": fallback_process_widget,
        "third_party_dependencies": third_party_dependencies_widget,
        "external_dependencies": external_dependencies_widget,
        "domain": domain_widget,
        "model_type": model_type_widget
    }

    # Group widgets into tabs for better organization
    tab_titles = ['Core Details', 'Operational Context']
    tab_contents = [
        widgets.VBox([
            core_widgets["model_id"],
            core_widgets["model_name"],
            core_widgets["model_version"],
            core_widgets["owner"],
            core_widgets["business_use"],
            core_widgets["domain"],
            core_widgets["model_type"]
        ]),
        widgets.VBox([
            core_widgets["intended_users"],
            core_widgets["model_outputs"],
            core_widgets["key_assumptions"],
            core_widgets["known_limitations"],
            core_widgets["fallback_process"],
            core_widgets["third_party_dependencies"],
            core_widgets["external_dependencies"]
        ])
    ]
    
    tabs = widgets.Tab(children=tab_contents)
    for i, title in enumerate(tab_titles):
        tabs.set_title(i, title)

    output_area = widgets.Output()
    submit_button = widgets.Button(description="Submit Core Metadata")

    def on_submit_button_clicked(b):
        with output_area:
            clear_output(wait=True)
            model_metadata = {k: v.value for k, v in core_widgets.items()}
            
            # Validate required fields
            missing_fields = [field for field in REQUIRED_FIELDS if field not in model_metadata or not model_metadata[field]]
            if missing_fields:
                print(f"Error: Missing required fields: {', '.join(missing_fields)}")
                return

            print("Core Model Metadata Captured:")
            for k, v in model_metadata.items():
                print(f"- {k}: {v}")
            
            # Store the metadata globally for subsequent steps
            global_model_metadata['core'] = model_metadata
            display(HTML("<hr>"))
            display(Markdown("### Core Metadata Captured. Proceed to **Assessing Inherent Risk Factors**."))

    submit_button.on_click(on_submit_button_clicked)
    
    display(tabs, submit_button, output_area)

# Initialize a global dictionary to store model metadata across cells
global_model_metadata = {}

# Call the UI function
get_model_metadata_ui(CONTROLLED_VOCABULARIES)
```

### Explanation of Execution

Alex has successfully used the interactive form to document the foundational details of the Predictive Maintenance Model. This ensures that essential information like its unique ID, owner, and business purpose are recorded in the enterprise model inventory, aligning with SR 11-7's guidance on comprehensive model documentation. The automated validation also highlighted required fields, enforcing data completeness from the start.

---

## 4. Assessing Inherent Risk Factors

Now that the core details are captured, Alex moves to assess the specific characteristics of the Predictive Maintenance Model that drive its inherent risk. This self-assessment is a proactive step in managing model risk, as emphasized in SR 11-7 (Section III, "Overview of Model Risk Management"). By evaluating factors like decision criticality and data sensitivity, Alex identifies potential adverse consequences, which is a key part of "inherent risk thinking" early in the model's lifecycle.

```python
def get_risk_driver_ui(controlled_vocab):
    """
    Generates a UI for capturing risk driver metadata using ipywidgets.
    Provides pre-filled values for the Predictive Maintenance Model's typical risk profile.
    """
    
    # Pre-filled risk driver data for the Predictive Maintenance Model
    initial_risk_drivers = {
        "decision_criticality": "Medium", # Predicting equipment failure is critical but typically allows for human intervention
        "data_sensitivity": "Internal", # Operational sensor data, not PII
        "automation_level": "Human-Approval", # Provides recommendations, human still approves
        "deployment_mode": "Human-in-loop", # Model results are reviewed by engineers before action
        "regulatory_materiality": "None" # Internal operational model, not directly impacting regulated areas
    }

    # Widget definitions for risk drivers
    decision_criticality_widget = widgets.Dropdown(description='Decision Criticality:', options=controlled_vocab["decision_criticality"], value=initial_risk_drivers["decision_criticality"])
    data_sensitivity_widget = widgets.Dropdown(description='Data Sensitivity:', options=controlled_vocab["data_sensitivity"], value=initial_risk_drivers["data_sensitivity"])
    automation_level_widget = widgets.Dropdown(description='Automation Level:', options=controlled_vocab["automation_level"], value=initial_risk_drivers["automation_level"])
    deployment_mode_widget = widgets.Dropdown(description='Deployment Mode:', options=controlled_vocab["deployment_mode"], value=initial_risk_drivers["deployment_mode"])
    regulatory_materiality_widget = widgets.Dropdown(description='Regulatory Materiality:', options=controlled_vocab["regulatory_materiality"], value=initial_risk_drivers["regulatory_materiality"])
    
    risk_widgets = {
        "decision_criticality": decision_criticality_widget,
        "data_sensitivity": data_sensitivity_widget,
        "automation_level": automation_level_widget,
        "deployment_mode": deployment_mode_widget,
        "regulatory_materiality": regulatory_materiality_widget
    }

    output_area = widgets.Output()
    submit_button = widgets.Button(description="Assess Risk Factors")

    def on_submit_button_clicked(b):
        with output_area:
            clear_output(wait=True)
            risk_drivers_data = {k: v.value for k, v in risk_widgets.items()}
            
            # Validate required fields (already handled implicitly by dropdowns having values)
            # but we can add an explicit check if needed, though for dropdowns it's less critical.
            
            # Consistency check example: Real-time fully automated with High criticality implies higher risk
            if (risk_drivers_data["automation_level"] == "Fully-Automated" and
                risk_drivers_data["deployment_mode"] == "Real-time" and
                risk_drivers_data["decision_criticality"] == "High"):
                print("Note: Fully automated real-time deployment with high decision criticality indicates heightened operational risk.")
            
            print("Inherent Risk Factors Captured:")
            for k, v in risk_drivers_data.items():
                print(f"- {k}: {v}")
            
            global_model_metadata['risk_drivers'] = risk_drivers_data
            display(HTML("<hr>"))
            display(Markdown("### Inherent Risk Factors Captured. Proceed to **Calculating Inherent Risk Score and Proposed Tier**."))

    submit_button.on_click(on_submit_button_clicked)
    
    display(widgets.VBox(list(risk_widgets.values())), submit_button, output_area)

# Call the UI function
get_risk_driver_ui(CONTROLLED_VOCABULARIES)
```

### Explanation of Execution

Alex has now specified the critical risk-driving attributes of the Predictive Maintenance Model. The selections (Medium criticality, Internal data, Human-Approval automation, Human-in-loop deployment, No regulatory materiality) reflect the current understanding of the model's operational context. This step is vital for a comprehensive model risk assessment, ensuring that potential sources of risk are identified early in the model's lifecycle, consistent with SR 11-7's principles on managing model risk magnitude.

---

## 5. Calculating Inherent Risk Score and Proposed Tier

With all the metadata and risk drivers in place, Alex proceeds to calculate the model's inherent risk score and determine its proposed tier. This process directly applies the deterministic tiering logic defined by Industrial Innovations Corp.'s MRM policy, derived from the concepts in LAB 3's "Tier Scoring (Deterministic)." This automated calculation provides an objective, initial assessment of the model's risk profile, informing subsequent MRM activities like validation depth and monitoring requirements.

```python
def calculate_inherent_risk(model_metadata, risk_scores, tier_thresholds):
    """
    Calculates the inherent risk score and determines the proposed risk tier
    based on the provided model metadata and scoring policy.
    
    Args:
        model_metadata (dict): Dictionary containing model risk driver metadata.
        risk_scores (dict): Dictionary defining points for each risk driver value.
        tier_thresholds (dict): Dictionary defining score cutoffs for each risk tier.
        
    Returns:
        dict: A dictionary containing the total risk score, proposed tier,
              and a detailed breakdown of points by factor.
    """
    
    total_score = 0
    score_breakdown = {}
    
    for driver, value in model_metadata.items():
        if driver in risk_scores:
            points = risk_scores[driver].get(value, 0) # Default to 0 if value not found
            total_score += points
            score_breakdown[driver] = {"value": value, "points": points}
            
    proposed_tier = "Unknown"
    tier_description = "N/A"
    
    # Determine the tier based on thresholds (higher tiers have higher min_score)
    sorted_tiers = sorted(tier_thresholds.items(), key=lambda item: item[1]["min_score"], reverse=True)
    for tier, details in sorted_tiers:
        if total_score >= details["min_score"]:
            proposed_tier = tier
            tier_description = details["description"]
            break
            
    return {
        "total_score": total_score,
        "proposed_tier": proposed_tier,
        "tier_description": tier_description,
        "score_breakdown": score_breakdown,
        "scoring_policy_version": SCORING_POLICY_VERSION,
        "assessment_timestamp": datetime.now().isoformat()
    }

# Ensure core and risk_drivers metadata are available
if 'core' in global_model_metadata and 'risk_drivers' in global_model_metadata:
    
    # Combine relevant metadata for risk calculation
    model_risk_data = global_model_metadata['risk_drivers']
    
    # Perform the risk calculation
    inherent_risk_assessment = calculate_inherent_risk(model_risk_data, RISK_SCORES, TIER_THRESHOLDS)
    
    # Store the assessment globally
    global_model_metadata['inherent_risk_assessment'] = inherent_risk_assessment
    
    display(Markdown("### Inherent Risk Assessment Results"))
    display(Markdown(f"**Model Name:** {global_model_metadata['core']['model_name']}"))
    display(Markdown(f"**Total Inherent Risk Score:** {inherent_risk_assessment['total_score']}"))
    display(Markdown(f"**Proposed Risk Tier:** <span style='font-size: 1.2em; font-weight: bold; color: {'red' if inherent_risk_assessment['proposed_tier'] == 'Tier 1' else 'orange' if inherent_risk_assessment['proposed_tier'] == 'Tier 2' else 'green'}'>{inherent_risk_assessment['proposed_tier']}</span>"))
    display(Markdown(f"**Tier Description:** {inherent_risk_assessment['tier_description']}"))
    display(Markdown(f"**Assessment Timestamp:** {inherent_risk_assessment['assessment_timestamp']}"))

    display(Markdown("\n#### Risk Factor Breakdown:"))
    breakdown_df = pd.DataFrame.from_dict(inherent_risk_assessment['score_breakdown'], orient='index')
    breakdown_df.index.name = 'Risk Driver'
    breakdown_df.rename(columns={'value': 'Selected Value', 'points': 'Points Contributed'}, inplace=True)
    display(breakdown_df)
    
    display(HTML("<hr>"))
    display(Markdown("### Inherent Risk Score and Tier Calculated. Proceed to **Documenting Owner's Narrative and Mitigations**."))

else:
    display(Markdown("Please ensure core model metadata and risk drivers are submitted in previous sections."))

```

### Explanation of Execution

Alex has successfully calculated the inherent risk score for the Predictive Maintenance Model. The breakdown clearly shows how each characteristic, such as 'Medium' decision criticality and 'Human-in-loop' deployment mode, contributed to the overall score. The model received a `Tier 2` classification, indicating moderate potential impact. This deterministic output provides a transparent basis for further discussion with the MRM team and aligns with SR 11-7's call for explainable tiering decisions.

---

## 6. Documenting Owner's Narrative and Mitigations

Alex's final task in this initial self-assessment is to provide a qualitative narrative, detailing their perspective on the model's risk, immediate mitigating factors, and any open questions for the MRM team. This narrative is crucial for "effective challenge" (SR 11-7, Section III) and provides vital context beyond quantitative scores, capturing the Model Owner's deeper understanding of the model's context and operational realities. It's the "preliminary risk narrative" that serves as a first input to the formal MRM process.

```python
def get_owner_narrative_ui():
    """
    Generates a UI for capturing the Model Owner's narrative and mitigations.
    """
    
    # Pre-filled narrative for the Predictive Maintenance Model
    initial_narrative = {
        "owner_risk_narrative": (
            "The Predictive Maintenance Model, while critical for operational efficiency, is designed with human-in-loop oversight. "
            "Its outputs serve as recommendations, requiring approval from maintenance engineers before any action. "
            "This significantly reduces the risk of incorrect automated decisions leading to adverse impacts. "
            "The model primarily uses internal sensor data, which is not sensitive from a privacy perspective."
        ),
        "immediate_mitigations": (
            "- Human-in-loop approval for all maintenance actions derived from model outputs.\n"
            "- Shadow mode deployment for 3 months post-initial validation to compare model recommendations with current practices.\n"
            "- Robust logging of model predictions and actual outcomes for continuous monitoring."
        ),
        "open_questions_for_mrm": (
            "- How should the model's performance be formally monitored post-deployment, and at what frequency?\n"
            "- What are the specific requirements for re-validation if the underlying equipment or operational context changes significantly?\n"
            "- Are there any specific data retention policies for sensor data used by this model?"
        )
    }

    owner_narrative_widget = widgets.Textarea(description='Owner Risk Narrative:', value=initial_narrative["owner_risk_narrative"], rows=6)
    immediate_mitigations_widget = widgets.Textarea(description='Immediate Mitigations:', value=initial_narrative["immediate_mitigations"], rows=5)
    open_questions_for_mrm_widget = widgets.Textarea(description='Open Questions for MRM:', value=initial_narrative["open_questions_for_mrm"], rows=5)
    
    narrative_widgets = {
        "owner_risk_narrative": owner_narrative_widget,
        "immediate_mitigations": immediate_mitigations_widget,
        "open_questions_for_mrm": open_questions_for_mrm_widget
    }

    output_area = widgets.Output()
    submit_button = widgets.Button(description="Submit Narrative & Mitigations")

    def on_submit_button_clicked(b):
        with output_area:
            clear_output(wait=True)
            narrative_data = {k: v.value for k, v in narrative_widgets.items()}
            
            print("Owner's Narrative and Mitigations Captured:")
            for k, v in narrative_data.items():
                print(f"- {k}:\n{v}\n")
            
            global_model_metadata['owner_narrative'] = narrative_data
            display(HTML("<hr>"))
            display(Markdown("### Narrative Captured. Proceed to **Final Review and Export of MRM Artifacts**."))

    submit_button.on_click(on_submit_button_clicked)
    
    display(widgets.VBox(list(narrative_widgets.values())), submit_button, output_area)

# Call the UI function
get_owner_narrative_ui()
```

### Explanation of Execution

Alex has articulated the qualitative aspects of the Predictive Maintenance Model's risk profile, complementing the quantitative score. The narrative highlights the human-in-the-loop design as a key control, while the listed mitigations and open questions provide a clear agenda for engagement with the MRM team. This rich context is invaluable for MRM personnel to conduct a thorough review and ensures that Alex, as the Model Owner, has proactively contributed to the model's overall risk management, as expected by SR 11-7.

---

## 7. Final Review and Export of MRM Artifacts

The final step for Alex is to consolidate all the collected information into a structured set of artifacts. These documents, including the detailed model registration and the inherent risk assessment, will be formally submitted to the Model Risk Management (MRM) team. This export ensures that all data is traceable, auditable, and ready for the next stages of the MRM process, adhering to the principles of documentation and record-keeping highlighted in SR 11-7 (Section VII, "Conclusion" and Section VI, "Model Inventory").

```python
def export_mrm_artifacts(model_details, output_dir="mrm_submission_artifacts"):
    """
    Exports the comprehensive model registration and risk assessment details
    into structured JSON and Markdown files.
    
    Args:
        model_details (dict): A dictionary containing all collected model metadata.
        output_dir (str): The directory to save the output files.
    """
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    model_id = model_details.get('core', {}).get('model_id', 'unknown_id')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. model_registration.json (contains all core, risk drivers, and assessment summary)
    full_registration_data = {
        "model_id": model_details.get('core', {}).get('model_id'),
        "model_name": model_details.get('core', {}).get('model_name'),
        "model_version": model_details.get('core', {}).get('model_version'),
        "owner": model_details.get('core', {}).get('owner'),
        "registration_timestamp": datetime.now().isoformat(),
        **model_details.get('core', {}), # Flatten core details
        **model_details.get('risk_drivers', {}), # Flatten risk drivers
        "inherent_risk_summary": {
            "total_score": model_details.get('inherent_risk_assessment', {}).get('total_score'),
            "proposed_tier": model_details.get('inherent_risk_assessment', {}).get('proposed_tier'),
            "tier_description": model_details.get('inherent_risk_assessment', {}).get('tier_description'),
            "scoring_policy_version": model_details.get('inherent_risk_assessment', {}).get('scoring_policy_version'),
            "assessment_timestamp": model_details.get('inherent_risk_assessment', {}).get('assessment_timestamp'),
        },
        "owner_narrative_summary": model_details.get('owner_narrative', {})
    }
    
    registration_json_path = os.path.join(output_dir, f"model_registration_{model_id}_{timestamp}.json")
    with open(registration_json_path, 'w') as f:
        json.dump(full_registration_data, f, indent=4)
        
    # 2. initial_inherent_risk_assessment.json (focused on risk calculation details)
    risk_assessment_json_path = os.path.join(output_dir, f"initial_inherent_risk_assessment_{model_id}_{timestamp}.json")
    with open(risk_assessment_json_path, 'w') as f:
        json.dump(model_details.get('inherent_risk_assessment', {}), f, indent=4)

    # 3. owner_narrative.md (Markdown file for human readability)
    narrative_md_path = os.path.join(output_dir, f"owner_narrative_{model_id}_{timestamp}.md")
    with open(narrative_md_path, 'w') as f:
        f.write(f"# Model Owner's Initial Risk Narrative for {model_details.get('core', {}).get('model_name')}\n\n")
        f.write(f"**Model ID:** {model_id}\n")
        f.write(f"**Owner:** {model_details.get('core', {}).get('owner')}\n")
        f.write(f"**Date of Assessment:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        
        f.write("## Inherent Risk Summary\n")
        f.write(f"**Proposed Risk Tier:** {model_details.get('inherent_risk_assessment', {}).get('proposed_tier')}\n")
        f.write(f"**Total Inherent Risk Score:** {model_details.get('inherent_risk_assessment', {}).get('total_score')}\n")
        f.write(f"**Tier Description:** {model_details.get('inherent_risk_assessment', {}).get('tier_description')}\n\n")

        f.write("## Owner's Risk Narrative\n")
        f.write(model_details.get('owner_narrative', {}).get('owner_risk_narrative', 'No narrative provided.') + "\n\n")
        
        f.write("## Immediate Mitigating Factors\n")
        f.write(model_details.get('owner_narrative', {}).get('immediate_mitigations', 'No immediate mitigations identified.') + "\n\n")
        
        f.write("## Open Questions for MRM Team\n")
        f.write(model_details.get('owner_narrative', {}).get('open_questions_for_mrm', 'No open questions.') + "\n")
        
    print(f"Artifacts exported to directory: {output_dir}")
    print(f"- Full Model Registration (JSON): {registration_json_path}")
    print(f"- Inherent Risk Assessment (JSON): {risk_assessment_json_path}")
    print(f"- Owner's Narrative (Markdown): {narrative_md_path}")
    
    # Preview the Markdown content
    display(Markdown("\n---"))
    display(Markdown("### Preview of `owner_narrative.md` content:"))
    with open(narrative_md_path, 'r') as f:
        display(Markdown(f.read()))


# Check if all necessary parts of the global_model_metadata are populated
if 'core' in global_model_metadata and 'risk_drivers' in global_model_metadata and 'inherent_risk_assessment' in global_model_metadata and 'owner_narrative' in global_model_metadata:
    export_mrm_artifacts(global_model_metadata)
    display(HTML("<hr>"))
    display(Markdown("### All MRM artifacts successfully generated and saved. This concludes the initial model registration and self-assessment for the Predictive Maintenance Model."))
else:
    display(Markdown("Please complete all previous sections to generate the full set of MRM artifacts."))
```

### Explanation of Execution

Alex has successfully compiled and exported all the required MRM artifacts. The JSON files provide machine-readable structured data for integration into enterprise systems, while the Markdown narrative offers a human-readable summary for MRM team review. This comprehensive package, complete with timestamps and policy versions, demonstrates adherence to Industrial Innovations Corp.'s MRM policies and the principles of transparency and auditability derived from SR 11-7. This deliverable serves as the official submission to formally initiate the MRM review process for the Predictive Maintenance Model.

