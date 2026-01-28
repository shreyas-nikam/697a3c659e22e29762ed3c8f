
# Model Registration & Initial Self-Assessment for Predictive Maintenance Model

## Introduction: Proactive Model Risk Management at Apex Financial Services

As a **System / Model Owner** at Apex Financial Services, your role is crucial in ensuring the responsible and compliant deployment of AI models. Today, you are tasked with registering a new "Predictive Maintenance Model" into the enterprise model inventory. This is not just a bureaucratic step; it's a fundamental part of our Model Risk Management (MRM) framework, directly addressing the principles outlined in **SR Letter 11-7**.

SR 11-7 emphasizes the importance of robust model development, implementation, and use, as well as comprehensive governance, policies, and controls. Specifically, Section IV ("Model Development, Implementation, and Use") highlights the need for disciplined processes, while Section VI ("Governance, Policies, and Controls") mandates maintaining a "comprehensive set of information for models implemented for use" (Page 20). Your initial model registration and self-assessment are the first line of defense, ensuring that potential model risks are identified and understood from the earliest stages of the model lifecycle. This proactive engagement helps us embed risk considerations at the source, saving time and reducing rework later, and fostering a culture of responsible AI.

This notebook will guide you through a simulated model registration interface, allowing you to input essential model metadata and then perform an initial, conceptual self-assessment of the model's inherent risk.

---

### **SR 11-7 Key Principles Addressed:**
- **Model Documentation:** Capturing comprehensive metadata about the model is essential for transparency and auditability (SR 11-7, Page 21).
- **Early Risk Thinking:** Identifying and assessing inherent risk characteristics at the registration stage ensures proactive management of potential adverse consequences (SR 11-7, Page 3).
- **Model Inventory:** Contributing to the firm-wide inventory of models by providing structured information about new models (SR 11-7, Page 20).
- **Owner Responsibilities:** As a Model Owner, you are accountable for providing accurate information and an initial risk assessment (SR 11-7, Page 18).

---

## 1. Setup and Dependencies

Before we begin the model registration process, we need to ensure all necessary libraries are installed and imported.

### Required Libraries Installation

We will use `uuid` for generating unique identifiers, `datetime` for timestamps, and `json` for structured data output. These are typically built-in or part of standard Python distributions, but we include `pandas` for potential future data structuring and `IPython.display` for rich output representation in a notebook.

```python
!pip install pandas # Install pandas for structured data handling
```

### Import Required Dependencies

```python
import uuid
import datetime
import json
import pandas as pd
from IPython.display import display, Markdown
```

## 2. Defining the Model Risk Assessment Framework

As a System/Model Owner, understanding how your model's characteristics translate into inherent risk is fundamental. Apex Financial Services uses a rule-based system to calculate an initial inherent risk score and assign a preliminary risk tier. This system considers several key factors defined by SR 11-7 and internal policies, helping us quantify the "magnitude" of model risk based on factors like "model complexity, higher uncertainty about inputs and assumptions, broader use, and larger potential impact" (SR 11-7, Page 4).

Our framework assigns points to specific categorical values for each risk factor. The total inherent risk score is then calculated as the sum of points from each factor.

Mathematically, the total inherent risk score $S_{total}$ is given by:

$$ S_{total} = \sum_{f \in \text{Factors}} P(V_f) $$

Where $P(V_f)$ is the points assigned to the chosen value $V_f$ for a given risk factor $f$.

The preliminary risk tier is determined by comparing $S_{total}$ against predefined thresholds. For example, if $T_1$, $T_2$, and $T_3$ are score thresholds for Tier 1, Tier 2, and Tier 3 respectively, then:

- If $S_{total} > T_1$, the model is Tier 1 (High Risk).
- If $T_2 < S_{total} \le T_1$, the model is Tier 2 (Medium Risk).
- If $S_{total} \le T_2$, the model is Tier 3 (Low Risk).

```python
# Define the scoring logic for inherent risk factors
# Each factor's categories are mapped to points
RISK_SCORING_TABLE = {
    'decision_criticality': {
        'Low': 1,
        'Medium': 3,
        'High': 5
    },
    'data_sensitivity': {
        'Public': 1,
        'Internal': 2,
        'Confidential': 3,
        'Regulated-PII': 5
    },
    'automation_level': {
        'Manual': 1,
        'Human-in-the-loop': 3,
        'Fully-Automated': 5
    },
    'regulatory_materiality': {
        'None': 1,
        'Low': 2,
        'Medium': 4,
        'High': 5
    }
}

# Define the thresholds for risk tiers
# Lower score means lower risk tier (e.g., Tier 3 is lowest risk)
TIER_THRESHOLDS = {
    'Tier 3': {'max_score': 8, 'description': 'Low Risk: Minimal impact, well-understood, or highly controlled.'},
    'Tier 2': {'max_score': 15, 'description': 'Medium Risk: Moderate impact, requires standard MRM oversight.'},
    'Tier 1': {'max_score': float('inf'), 'description': 'High Risk: Significant impact, requires extensive MRM oversight.'}
}

SCORING_VERSION = "v1.0"

# Display the scoring table and tier thresholds for transparency
display(Markdown("### Inherent Risk Scoring Table"))
display(pd.DataFrame(RISK_SCORING_TABLE).fillna('-').T)

display(Markdown("### Proposed Risk Tier Thresholds"))
tier_df = pd.DataFrame.from_dict(TIER_THRESHOLDS, orient='index')
tier_df.index.name = 'Tier'
display(tier_df)
```

## 3. Registering the Predictive Maintenance Model: Metadata Input

As the Model Owner, Alex Chen, your first task is to input the comprehensive metadata for the "Predictive Maintenance Model." This detailed documentation is critical, as highlighted in SR 11-7 Section VI ("Governance, Policies, and Controls") and specifically regarding "Model Inventory" (Page 20), which states, "Without adequate documentation, model risk assessment and management will be ineffective." This initial data forms the foundation for all subsequent MRM activities, ensuring clarity on the model's purpose, scope, and technical characteristics.

You will define the model's attributes using a Python dictionary, simulating the input process of a structured registration interface. Pay close attention to the controlled vocabularies for risk factors, as these will directly influence the inherent risk score.

```python
def register_model_metadata(model_details: dict) -> dict:
    """
    Registers the model metadata, including generating audit fields.

    Args:
        model_details (dict): A dictionary containing the model's core metadata.

    Returns:
        dict: The complete model registration record with audit fields.
    """
    # Validate required fields
    required_fields = [
        'model_name', 'business_use', 'domain', 'model_type',
        'decision_criticality', 'data_sensitivity', 'automation_level',
        'regulatory_materiality'
    ]
    for field in required_fields:
        if field not in model_details or not model_details[field]:
            raise ValueError(f"Required field '{field}' is missing or empty.")

    # Enforce controlled vocabularies for risk factors
    for factor, allowed_values in RISK_SCORING_TABLE.items():
        if factor in model_details and model_details[factor] not in allowed_values:
            raise ValueError(f"Invalid value '{model_details[factor]}' for '{factor}'. "
                             f"Allowed values are: {', '.join(allowed_values.keys())}")

    # Generate model_id if not provided (assume it's generated by the system)
    if 'model_id' not in model_details or not model_details['model_id']:
        model_details['model_id'] = str(uuid.uuid4())

    # Add audit fields
    model_details['created_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    model_details['created_by'] = 'Alex Chen (System/Model Owner)'
    model_details['lab_version'] = '1.0'

    return model_details

# Alex Chen inputs the metadata for the Predictive Maintenance Model
predictive_maintenance_model_metadata = {
    'model_name': 'Predictive Maintenance Model v2.1',
    'business_use': 'Predict equipment failure in manufacturing to optimize maintenance schedules and reduce downtime.',
    'domain': 'Operations Efficiency',
    'model_type': 'ML classifier (time-series)',
    'decision_criticality': 'High',  # If equipment fails, production stops, high financial impact
    'data_sensitivity': 'Internal', # Uses internal operational data, not PII
    'automation_level': 'Fully-Automated', # Model directly triggers alerts/actions without human gate
    'deployment_mode': 'Real-time',
    'regulatory_materiality': 'None', # Not directly tied to financial reporting or customer interaction
    'owner_team': 'Manufacturing Operations Analytics'
}

# Execute the registration function
try:
    registered_model = register_model_metadata(predictive_maintenance_model_metadata)
    display(Markdown("### Model Metadata Successfully Registered:"))
    display(registered_model)
except ValueError as e:
    print(f"Error during model registration: {e}")
    registered_model = None

```

## 4. Inherent Risk Self-Assessment: Calculating Score and Tier

With the model metadata captured, the next step for Alex is to perform the initial inherent risk self-assessment. This involves applying the predefined scoring logic to the model's characteristics (e.g., `decision_criticality`, `data_sensitivity`). This step allows Alex to "assess the magnitude" of model risk, a core activity in model risk management according to SR 11-7 (Page 4). Understanding the inherent risk helps in determining the appropriate level of scrutiny and governance required for the model.

The function `calculate_inherent_risk` will:
1. Iterate through the defined risk factors.
2. For each factor, retrieve the assigned points based on the model's metadata.
3. Sum these points to get the `inherent_risk_score`.
4. Determine the `proposed_risk_tier` based on the score and predefined thresholds.
5. Provide a `score_breakdown` for transparency and explainability.

```python
def calculate_inherent_risk(model_metadata: dict, scoring_table: dict, tier_thresholds: dict, scoring_version: str) -> dict:
    """
    Calculates the inherent risk score and proposed tier for a model based on its metadata.

    Args:
        model_metadata (dict): The registered model's metadata.
        scoring_table (dict): The predefined scoring logic for risk factors.
        tier_thresholds (dict): The predefined thresholds for risk tiers.
        scoring_version (str): The version of the scoring logic used.

    Returns:
        dict: A dictionary containing the inherent risk score, proposed tier, and score breakdown.
    """
    inherent_risk_score = 0
    score_breakdown = {}

    for factor, score_map in scoring_table.items():
        if factor in model_metadata:
            value = model_metadata[factor]
            if value in score_map:
                points = score_map[value]
                inherent_risk_score += points
                score_breakdown[factor] = {'value': value, 'points': points}
            else:
                # This case should ideally be caught by initial validation in register_model_metadata
                score_breakdown[factor] = {'value': value, 'points': 0, 'warning': 'Value not found in scoring map.'}
        else:
            score_breakdown[factor] = {'value': 'N/A', 'points': 0, 'warning': f'Factor "{factor}" not in model metadata.'}

    proposed_risk_tier = 'Undefined'
    tier_description = 'No tier assigned.'
    for tier, data in tier_thresholds.items():
        if inherent_risk_score <= data['max_score']:
            proposed_risk_tier = tier
            tier_description = data['description']
            break

    return {
        'inherent_risk_score': inherent_risk_score,
        'proposed_risk_tier': proposed_risk_tier,
        'proposed_tier_description': tier_description,
        'score_breakdown': score_breakdown,
        'scoring_version': scoring_version
    }

# Execute the risk assessment for the registered model
if registered_model:
    risk_assessment = calculate_inherent_risk(registered_model, RISK_SCORING_TABLE, TIER_THRESHOLDS, SCORING_VERSION)
    registered_model.update(risk_assessment) # Add risk assessment results to the model record

    display(Markdown("### Inherent Risk Self-Assessment Results:"))
    display(Markdown(f"**Total Inherent Risk Score:** `{registered_model['inherent_risk_score']}`"))
    display(Markdown(f"**Proposed Risk Tier:** `{registered_model['proposed_risk_tier']}` - *{registered_model['proposed_tier_description']}*"))

    display(Markdown("#### Score Breakdown by Factor:"))
    breakdown_df = pd.DataFrame([
        {'Factor': k, 'Value': v['value'], 'Points': v['points']}
        for k, v in registered_model['score_breakdown'].items()
    ])
    display(breakdown_df)
else:
    print("Cannot perform risk assessment: Model registration failed.")
```

### Explanation of Execution

The output above provides a clear breakdown of how the `Predictive Maintenance Model`'s characteristics contribute to its inherent risk. For Alex Chen, this is invaluable. For instance, the "High" `decision_criticality` and "Fully-Automated" `automation_level` contribute significantly to the total score, directly reflecting the potential adverse consequences if the model is inaccurate or misused, as described in SR 11-7 (Page 3).

The calculated `proposed_risk_tier` (e.g., Tier 2 or Tier 1) gives Alex an immediate understanding of the model's preliminary risk profile. This initial tier assignment is crucial for setting expectations for downstream governance processes and aligning with the principle of "proportionality," where "the rigor and sophistication of validation should be commensurate with the bank's overall use of models, the complexity and materiality of its models" (SR 11-7, Page 9). Knowing the tier early helps the Model Owner anticipate the level of MRM scrutiny and resource allocation required.

## 5. Model Owner's Narrative: Justification and Open Questions

The quantitative risk score provides a structured view, but qualitative insights from the Model Owner are equally important. Alex Chen, as the System/Model Owner, must now provide a narrative justification for the proposed tier, highlight any immediate mitigating factors, and list any open questions for the Model Risk Management (MRM) team. This qualitative input ensures that context, domain expertise, and ongoing considerations are captured, fulfilling the requirement for model owners to "provide all necessary information for validation activities" (SR 11-7, Page 18) and contributing to comprehensive documentation (SR 11-7, Page 21).

This narrative serves as a critical bridge between the model's technical specifications and its real-world operational context, allowing for a holistic risk assessment.

```python
def add_owner_narrative(model_record: dict, narrative: str, mitigations: str = None, open_questions: str = None) -> dict:
    """
    Adds the Model Owner's narrative and qualitative assessment to the model record.

    Args:
        model_record (dict): The complete model registration record.
        narrative (str): Justification for the proposed tier.
        mitigations (str, optional): Immediate mitigating factors.
        open_questions (str, optional): Open questions for the MRM team.

    Returns:
        dict: The updated model record with narrative fields.
    """
    if not narrative:
        raise ValueError("Owner risk narrative is a required field.")

    model_record['owner_risk_narrative'] = narrative
    if mitigations:
        model_record['owner_mitigations'] = mitigations
    if open_questions:
        model_record['owner_open_questions_for_mrm'] = open_questions

    return model_record

# Alex Chen provides the narrative
if registered_model:
    owner_narrative = (
        "The proposed Tier 1 is reasonable given the model's fully-automated deployment and direct "
        "impact on critical manufacturing processes. While the model currently focuses on internal "
        "operational efficiency (explaining 'Internal' data sensitivity and 'None' regulatory materiality), "
        "a failure could lead to significant financial losses due to production halts. "
        "The model's output directly informs maintenance scheduling, which has a 'High' criticality."
    )
    owner_mitigations = (
        "The model is monitored 24/7 by the operations team. There are manual override mechanisms "
        "in place, and alerts are reviewed by a human operator before significant actions are taken. "
        "The model retraining frequency is quarterly, and performance drift is actively tracked."
    )
    owner_open_questions = (
        "1. What is the expected cadence for full model validation by the MRM team for a Tier 1 model? "
        "2. Are there specific performance metrics or benchmarks MRM would like to see included in ongoing monitoring?"
    )

    try:
        final_model_registration = add_owner_narrative(
            registered_model, owner_narrative, owner_mitigations, owner_open_questions
        )
        display(Markdown("### Model Owner's Narrative Added:"))
        display(Markdown(f"**Justification:** {final_model_registration['owner_risk_narrative']}"))
        if 'owner_mitigations' in final_model_registration:
            display(Markdown(f"**Mitigating Factors:** {final_model_registration['owner_mitigations']}"))
        if 'owner_open_questions_for_mrm' in final_model_registration:
            display(Markdown(f"**Open Questions for MRM:** {final_model_registration['owner_open_questions_for_mrm']}"))
    except ValueError as e:
        print(f"Error adding narrative: {e}")
        final_model_registration = registered_model # Retain previous state if narrative fails
else:
    print("Cannot add owner narrative: Model registration or risk assessment failed.")
    final_model_registration = None
```

### Explanation of Execution

By adding the narrative, Alex translates the quantitative risk score into a richer, qualitative context. This markdown output directly displays the Model Owner's rationale, highlighting specific operational details and existing controls (mitigations) that an automated scoring system might not fully capture. This nuanced input is invaluable for the MRM team, providing a complete picture of the model's risk profile and demonstrating Alex's proactive engagement with model risk, in line with SR 11-7's emphasis on effective challenge and comprehensive risk understanding (SR 11-7, Page 4 & 5). The open questions also show a proactive approach to engaging with MRM, fostering collaborative risk management.

## 6. Finalizing and Exporting the Model Registration Artifact

The final step for Alex is to consolidate all the collected metadata, the computed risk assessment, and the owner's narrative into a single, structured artifact. This canonical JSON output serves as the official record of the model's initial registration and self-assessment, designed to be stable and portable for downstream processes, such as feeding into Lab 2 of the MRM workflow. This action directly addresses SR 11-7's guidance on "Model Inventory" which requires "maintenance of detailed documentation of all aspects of the model risk management framework, including an inventory of models in use" (Page 18) and the importance of auditability.

```python
def export_model_registration_artifact(model_record: dict, filename: str = 'lab1_model_registration.json'):
    """
    Exports the complete model registration record to a JSON file.

    Args:
        model_record (dict): The complete model registration record.
        filename (str): The name of the JSON file to save.
    """
    if not model_record:
        print("No model record to export. Registration might have failed.")
        return

    try:
        with open(filename, 'w') as f:
            json.dump(model_record, f, indent=4)
        display(Markdown(f"### Model Registration Artifact Exported:"))
        display(Markdown(f"Successfully saved the complete model registration data to `{filename}`."))
        display(Markdown("This JSON file contains all metadata, computed risk scores, and the Model Owner's narrative, ready for ingestion by downstream MRM processes."))
    except IOError as e:
        print(f"Error exporting model registration artifact: {e}")

# Specify the output filename
output_filename = 'lab1_predictive_maintenance_model_registration.json'

# Execute the export function
if final_model_registration:
    export_model_registration_artifact(final_model_registration, output_filename)
else:
    print("Cannot export artifact: Model registration, risk assessment, or narrative addition failed.")
```

### Explanation of Execution

The saved JSON file (`lab1_predictive_maintenance_model_registration.json`) represents the formal completion of the initial model registration and self-assessment. For Alex Chen, this is a tangible deliverable that ensures the "Predictive Maintenance Model" is properly onboarded into Apex Financial Services' MRM framework. This structured artifact fulfills the auditability requirements of SR 11-7 by providing a clear, immutable record of the model's status at this stage. It's now ready for review by the MRM team, serving as a critical input for the next phases of model governance and validation.

```json
{
    "model_name": "Predictive Maintenance Model v2.1",
    "business_use": "Predict equipment failure in manufacturing to optimize maintenance schedules and reduce downtime.",
    "domain": "Operations Efficiency",
    "model_type": "ML classifier (time-series)",
    "decision_criticality": "High",
    "data_sensitivity": "Internal",
    "automation_level": "Fully-Automated",
    "deployment_mode": "Real-time",
    "regulatory_materiality": "None",
    "owner_team": "Manufacturing Operations Analytics",
    "model_id": "a_unique_uuid_will_be_generated_here",
    "created_at": "2023-10-27T10:00:00.000000+00:00",
    "created_by": "Alex Chen (System/Model Owner)",
    "lab_version": "1.0",
    "inherent_risk_score": 11,
    "proposed_risk_tier": "Tier 2",
    "proposed_tier_description": "Medium Risk: Moderate impact, requires standard MRM oversight.",
    "score_breakdown": {
        "decision_criticality": {
            "value": "High",
            "points": 5
        },
        "data_sensitivity": {
            "value": "Internal",
            "points": 2
        },
        "automation_level": {
            "value": "Fully-Automated",
            "points": 5
        },
        "regulatory_materiality": {
            "value": "None",
            "points": 1
        }
    },
    "scoring_version": "v1.0",
    "owner_risk_narrative": "The proposed Tier 1 is reasonable given the model's fully-automated deployment and direct impact on critical manufacturing processes. While the model currently focuses on internal operational efficiency (explaining 'Internal' data sensitivity and 'None' regulatory materiality), a failure could lead to significant financial losses due to production halts. The model's output directly informs maintenance scheduling, which has a 'High' criticality.",
    "owner_mitigations": "The model is monitored 24/7 by the operations team. There are manual override mechanisms in place, and alerts are reviewed by a human operator before significant actions are taken. The model retraining frequency is quarterly, and performance drift is actively tracked.",
    "owner_open_questions_for_mrm": "1. What is the expected cadence for full model validation by the MRM team for a Tier 1 model? 2. Are there specific performance metrics or benchmarks MRM would like to see included in ongoing monitoring?"
}
```
*Note: The `model_id` and `created_at` in the above JSON example are illustrative; actual values will be dynamically generated.*
