
# Predictive Maintenance Model Registration & Initial Risk Self-Assessment (SR 11-7)

**Persona:** Alex Chen, System / Model Owner at TechCo  
**Organization:** TechCo, a leader in industrial automation and smart manufacturing.  
**Case Study:** Alex is bringing a new AI model, the "Predictive Maintenance Model," into production. Before its official launch, Alex must register the model in TechCo's enterprise model inventory and conduct an initial self-assessment of its inherent risk characteristics. This process is crucial for complying with TechCo's internal Model Risk Management (MRM) policies, which are inspired by regulatory guidelines like SR 11-7, specifically Section IV: "Model Development, Implementation, and Use." This early assessment helps TechCo proactively manage potential model risks, ensuring responsible AI development and operational compliance.

---

## 1. Setting up the Model Registration Environment

### Story + Context + Real-World Relevance

Alex begins by setting up the necessary tools and defining TechCo's standardized framework for model registration and initial risk assessment. This framework includes explicit definitions for model metadata, a deterministic scoring mechanism for inherent risk factors, and clear thresholds for assigning a preliminary risk tier. This systematic approach, as emphasized in SR 11-7, ensures consistency, transparency, and auditability in the model lifecycle, enabling effective challenge and governance from the earliest stages.

The deterministic scoring mechanism is based on assigning points to specific categorical values of inherent risk attributes. The total score is then mapped to a risk tier. This transparency is vital for explaining risk decisions to stakeholders, as highlighted in SR 11-7's emphasis on "sound model development, implementation, and use" and the need for clear documentation (SR 11-7, Section IV, Page 5, and Section VI, Page 21).

### Code cell (function definition + function execution)

```python
import json
import uuid
import datetime
import pandas as pd

# Define the scoring logic for inherent risk factors
RISK_SCORING_CONFIG = {
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
        'Advisory': 1,
        'Semi': 3,
        'Fully-Automated': 5
    },
    'deployment_mode': {
        'Internal-only': 1, # Similar to Batch for risk impact
        'Batch': 1,
        'Human-in-loop': 2,
        'Real-time': 4
    },
    'regulatory_materiality': {
        'None': 1,
        'Moderate': 3,
        'High': 5
    }
}

# Define the risk tier thresholds (from Lab 3 attachment, Page 4)
RISK_TIER_THRESHOLDS = {
    'Tier 1': {'min_score': 22, 'description': 'Very High Risk: Requires extensive validation and stringent controls.'},
    'Tier 2': {'min_score': 15, 'description': 'Moderate Risk: Requires thorough validation and enhanced controls.'},
    'Tier 3': {'min_score': 0,  'description': 'Low Risk: Requires standard validation and basic controls.'} # min_score 0 for anything below Tier 2
}

def calculate_initial_risk_score_and_tier(model_metadata):
    """
    Calculates the initial inherent risk score and assigns a preliminary tier based on
    predefined scoring logic and tier thresholds.

    Args:
        model_metadata (dict): A dictionary containing model metadata, including
                                inherent risk factors like 'decision_criticality',
                                'data_sensitivity', 'automation_level',
                                'deployment_mode', and 'regulatory_materiality'.

    Returns:
        tuple: A tuple containing:
            - total_score (int): The calculated total inherent risk score.
            - preliminary_tier (str): The assigned preliminary risk tier (e.g., 'Tier 1').
            - score_breakdown (dict): A breakdown of scores by each factor.
    """
    total_score = 0
    score_breakdown = {}

    # Calculate score for each factor
    for factor, values in RISK_SCORING_CONFIG.items():
        if factor in model_metadata and model_metadata[factor] in values:
            score = values[model_metadata[factor]]
            total_score += score
            score_breakdown[factor] = {'value': model_metadata[factor], 'score': score}
        else:
            # Handle cases where a factor is missing or value is invalid, assigning a default low score or flagging
            # For this lab, we assume valid inputs for simplicity.
            score_breakdown[factor] = {'value': model_metadata.get(factor, 'N/A'), 'score': 0}

    # Determine the preliminary risk tier
    preliminary_tier = 'Tier 3' # Default to lowest tier
    for tier, thresholds in sorted(RISK_TIER_THRESHOLDS.items(), key=lambda item: item[1]['min_score'], reverse=True):
        if total_score >= thresholds['min_score']:
            preliminary_tier = tier
            break

    return total_score, preliminary_tier, score_breakdown

# No direct execution of the core logic function yet, as we need to define model metadata first.
# This cell serves to define the framework for subsequent sections.
```

### Explanation of Execution

This code defines the core logic that Alex will use throughout the self-assessment. `RISK_SCORING_CONFIG` and `RISK_TIER_THRESHOLDS` are crucial elements of TechCo's MRM policy, enabling a standardized and explainable approach to risk tiering. The `calculate_initial_risk_score_and_tier` function is designed to take model metadata and apply this deterministic logic. This standardization directly supports SR 11-7's call for clear policies and procedures to manage model risk effectively (SR 11-7, Section VI, Page 17). The explicit point assignments and thresholds ensure that the risk assessment is objective and reproducible.

---

## 2. Registering Core Model Identity and Purpose

### Story + Context + Real-World Relevance

Alex's first task is to formally register the "Predictive Maintenance Model" by providing its fundamental identity and purpose. This step is equivalent to creating an entry in TechCo's central model inventory, a critical requirement for any organization managing AI at scale. SR 11-7 emphasizes the importance of a comprehensive model inventory that describes the model's purpose, intended use, and other key identifiers (SR 11-7, Section VI, Model Inventory, Page 20). This initial documentation is foundational for all subsequent MRM activities, including validation, monitoring, and change control.

### Code cell (function definition + function execution)

```python
def register_core_metadata(model_name, version, owner, business_unit, business_use, domain, model_type, intended_users=None, decision_context=None):
    """
    Registers the core identifying and purpose-related metadata for a new model.

    Args:
        model_name (str): The name of the model.
        version (str): The version of the model (e.g., "1.0", "beta").
        owner (str): The primary owner of the model (persona).
        business_unit (str): The business unit responsible for the model.
        business_use (str): A description of the model's business application.
        domain (str): The operational domain (e.g., 'finance', 'healthcare', 'engineering').
        model_type (str): The type of AI model (e.g., 'ML', 'LLM', 'AGENT').
        intended_users (list, optional): List of intended user roles or departments.
        decision_context (str, optional): The context in which decisions are made using the model.

    Returns:
        dict: A dictionary containing the registered core metadata.
    """
    model_id = str(uuid.uuid4()) # Generate a unique model ID

    core_metadata = {
        'model_id': model_id,
        'model_name': model_name,
        'version': version,
        'owner': owner,
        'business_unit': business_unit,
        'business_use': business_use,
        'domain': domain,
        'model_type': model_type,
        'intended_users': intended_users if intended_users is not None else [],
        'decision_context': decision_context,
        'created_at': datetime.datetime.now().isoformat()
    }
    return core_metadata

# Alex registers the Predictive Maintenance Model
predictive_maintenance_model = register_core_metadata(
    model_name="Predictive Maintenance Model",
    version="1.0",
    owner="Alex Chen",
    business_unit="Manufacturing Operations",
    business_use="Predict equipment failures in manufacturing lines to enable proactive maintenance and minimize downtime.",
    domain="engineering",
    model_type="ML",
    intended_users=["Maintenance Technicians", "Operations Managers"],
    decision_context="Alerting mechanism for maintenance scheduling and resource allocation."
)

print(json.dumps(predictive_maintenance_model, indent=2))
```

### Explanation of Execution

Alex has successfully registered the core details of the "Predictive Maintenance Model." The `model_id` provides a unique identifier, essential for tracking within TechCo's enterprise model inventory. The `business_use` and `domain` fields clearly articulate the model's purpose, directly addressing SR 11-7's guidance that "an effective development process begins with a clear statement of purpose to ensure that model development is aligned with the intended use" (SR 11-7, Section IV, Page 5). This output serves as the foundational record for the model's entry into the MRM system.

---

## 3. Detailing Model Implementation & Operational Basics

### Story + Context + Real-World Relevance

After establishing the core identity, Alex now provides details about how the Predictive Maintenance Model is implemented and its operational context. This includes specifying the algorithm family, training approach, and crucial operational details like owner and fallback processes. These details contribute to a holistic understanding of the model, which is critical for assessing potential operational risks and ensuring the model can be effectively managed throughout its lifecycle. SR 11-7 emphasizes that "sound model risk management depends on substantial investment in supporting systems to ensure data and reporting integrity, together with controls and testing to ensure proper implementation of models, effective systems integration, and appropriate use" (SR 11-7, Section IV, Page 7).

### Code cell (function definition + function execution)

```python
def add_implementation_details(model_record, algorithm_family, training_approach, deployment_owner, upstream_systems, downstream_systems, fallback_process):
    """
    Adds implementation and operational details to the model registration record.

    Args:
        model_record (dict): The existing model registration dictionary.
        algorithm_family (str): The family of algorithms used (e.g., 'Gradient Boosting', 'Deep Learning').
        training_approach (str): How the model is trained ('batch', 'online', 'transfer learning').
        deployment_owner (str): The team or individual responsible for technical deployment.
        upstream_systems (list): Systems providing data to this model.
        downstream_systems (list): Systems consuming outputs from this model.
        fallback_process (str): Description of the process if the model fails or is unavailable.

    Returns:
        dict: The updated model registration dictionary.
    """
    model_record.update({
        'algorithm_family': algorithm_family,
        'training_approach': training_approach,
        'deployment_owner': deployment_owner,
        'upstream_systems': upstream_systems,
        'downstream_systems': downstream_systems,
        'fallback_process': fallback_process
    })
    return model_record

# Alex adds implementation and operational details
predictive_maintenance_model = add_implementation_details(
    predictive_maintenance_model,
    algorithm_family="Gradient Boosting",
    training_approach="batch",
    deployment_owner="ML Engineering Team A",
    upstream_systems=["Sensor Data Lake", "ERP System"],
    downstream_systems=["Maintenance Scheduling System", "Operations Dashboard"],
    fallback_process="Manual equipment inspection and rule-based alarming."
)

print(json.dumps(predictive_maintenance_model, indent=2))
```

### Explanation of Execution

The model record now includes details about its technical implementation and operational dependencies. Knowing the `algorithm_family` and `training_approach` helps the MRM team understand the model's inherent complexity and potential failure modes. Furthermore, identifying `upstream_systems`, `downstream_systems`, and a `fallback_process` is crucial for assessing its integration risks and business continuity, aligning with SR 11-7's focus on robust model implementation and use, especially concerning data flow and system interdependencies (SR 11-7, Section IV, Page 7).

---

## 4. Assessing Inherent Risk Factors

### Story + Context + Real-World Relevance

Now, Alex dives into the core of the self-assessment: evaluating the model's inherent risk drivers. This involves carefully considering the `decision_criticality` (how impactful its decisions are), `data_sensitivity` (the nature of data it processes), `automation_level` (degree of human intervention), `deployment_mode` (real-time vs. batch), and `regulatory_materiality` (regulatory implications). This self-assessment is a proactive measure to understand and document the model's risk profile from the perspective of the First Line of Defense, a key expectation of SR 11-7's "Model Development, Implementation, and Use" section (SR 11-7, Section IV, Page 5). Understanding these factors is critical for later determining the appropriate level of validation and oversight.

### Code cell (function definition + function execution)

```python
def add_inherent_risk_factors(model_record, decision_criticality, data_sensitivity, automation_level, deployment_mode, regulatory_materiality):
    """
    Adds the inherent risk factors to the model registration record.

    Args:
        model_record (dict): The existing model registration dictionary.
        decision_criticality (str): Impact of model decisions ('Low', 'Medium', 'High').
        data_sensitivity (str): Sensitivity of data used ('Public', 'Internal', 'Confidential', 'Regulated-PII').
        automation_level (str): Degree of human intervention ('Advisory', 'Semi', 'Fully-Automated').
        deployment_mode (str): How the model is deployed ('Internal-only', 'Batch', 'Human-in-loop', 'Real-time').
        regulatory_materiality (str): Regulatory impact ('None', 'Moderate', 'High').

    Returns:
        dict: The updated model registration dictionary.
    """
    # Basic validation for allowed values
    for factor, allowed_values in RISK_SCORING_CONFIG.items():
        input_value = locals()[factor] # Get the value of the parameter with the same name
        if input_value not in allowed_values:
            raise ValueError(f"Invalid value '{input_value}' for '{factor}'. Must be one of {list(allowed_values.keys())}")

    model_record.update({
        'decision_criticality': decision_criticality,
        'data_sensitivity': data_sensitivity,
        'automation_level': automation_level,
        'deployment_mode': deployment_mode,
        'regulatory_materiality': regulatory_materiality
    })
    return model_record

# Alex assesses and adds the inherent risk factors for the Predictive Maintenance Model
predictive_maintenance_model = add_inherent_risk_factors(
    predictive_maintenance_model,
    decision_criticality="Medium",      # Predicts failure; alerts for human action; impacts operational uptime.
    data_sensitivity="Internal",       # Uses proprietary sensor data, but no PII.
    automation_level="Semi",           # Generates alerts, but human technicians make final maintenance decisions.
    deployment_mode="Real-time",       # Needs to detect anomalies and alert quickly for proactive maintenance.
    regulatory_materiality="None"      # Primarily internal operational efficiency, no direct external regulatory reporting.
)

print(json.dumps(predictive_maintenance_model, indent=2))
```

### Explanation of Execution

The `predictive_maintenance_model` record now contains the crucial inherent risk factors. Alex's careful assessment of these categories provides the necessary inputs for TechCo's deterministic tiering logic. Each choice reflects a judgment about the model's potential for adverse consequences, directly linking to SR 11-7's definition of "model risk" as "the potential for adverse consequences from decisions based on incorrect or misused model outputs" (SR 11-7, Section III, Page 3). This data forms the basis for quantitative risk scoring.

---

## 5. Calculating Initial Risk Score and Assigning Preliminary Tier

### Story + Context + Real-World Relevance

With all relevant metadata and inherent risk factors documented, Alex now uses TechCo's standardized scoring mechanism to compute an initial risk score and assign a preliminary risk tier. This quantitative assessment provides an objective, first-pass understanding of the model's risk profile. The process follows TechCo's established "Tier Scoring (Deterministic)" methodology, as described in the lab brief and consistent with Lab 3's core logic. The total risk score, denoted as $\text{Total Risk Score}$, is calculated as the sum of individual scores from each inherent risk factor.

$$ \text{Total Risk Score} = S_{\text{criticality}} + S_{\text{sensitivity}} + S_{\text{automation}} + S_{\text{deployment}} + S_{\text{regulatory}} $$

where $S_X$ represents the score assigned to the chosen value of risk factor $X$.  
This score is then mapped to a tier using predefined thresholds:
- Tier 1: $\text{Total Risk Score} \geq 22$
- Tier 2: $\text{Total Risk Score} \geq 15$
- Tier 3: $\text{Total Risk Score} < 15$

This transparent tiering is essential for explaining risk decisions and aligning the model with appropriate levels of validation rigor and oversight, a core tenet of SR 11-7 (SR 11-7, Section VII, Page 21: "practical application of this guidance should be commensurate with a bank's risk exposures, its business activities, and the extent and complexity of its model use.").

### Code cell (function definition + function execution)

```python
# Execute the previously defined scoring function
total_score, preliminary_tier, score_breakdown = calculate_initial_risk_score_and_tier(predictive_maintenance_model)

predictive_maintenance_model['initial_risk_score'] = total_score
predictive_maintenance_model['preliminary_risk_tier'] = preliminary_tier
predictive_maintenance_model['score_breakdown'] = score_breakdown

print(f"Calculated Initial Risk Score: {total_score}")
print(f"Proposed Preliminary Risk Tier: {preliminary_tier}")
print("\nScore Breakdown:")
for factor, details in score_breakdown.items():
    print(f"  - {factor}: {details['value']} (Score: {details['score']})")

print(f"\nFull Model Registration (with scoring results):\n{json.dumps(predictive_maintenance_model, indent=2)}")

# Display tiering rationale for persona's understanding
tier_description = RISK_TIER_THRESHOLDS[preliminary_tier]['description']
print(f"\nTier Rationale for {preliminary_tier}: {tier_description}")
```

### Explanation of Execution

The "Predictive Maintenance Model" has an `initial_risk_score` of 13, resulting in a `preliminary_risk_tier` of 'Tier 3'. The score breakdown clearly shows how each inherent risk factor contributed to the total. For Alex, this outcome is important: a Tier 3 model typically implies standard, less intensive validation and control requirements compared to higher-tier models. This objective, quantitative assessment helps Alex articulate the model's risk profile to the MRM team and ensures compliance with TechCo's framework for aligning validation efforts with the model's inherent risk, as per SR 11-7 principles of proportionality (SR 11-7, Section V, Page 9: "The rigor and sophistication of validation should be commensurate with the bank's overall use of models, the complexity and materiality of its models, and the size and complexity of the bank's operations.").

---

## 6. Documenting Model Owner's Risk Narrative

### Story + Context + Real-World Relevance

The quantitative score provides a baseline, but Alex's expertise as the Model Owner is crucial for a complete risk picture. Alex must now add a qualitative narrative, elaborating on the model's known limitations, initial mitigation strategies, and any open questions for the MRM team. This narrative serves as the Model Owner's preliminary risk assessment and justification, offering context beyond the numbers. This step directly supports SR 11-7's emphasis on comprehensive documentation and the importance of user insights: "Documentation of model development and validation should be sufficiently detailed so that parties unfamiliar with a model can understand how the model operates, its limitations, and its key assumptions" (SR 11-7, Section VI, Documentation, Page 21).

### Code cell (function definition + function execution)

```python
def add_owner_risk_narrative(model_record, owner_risk_narrative, known_limitations=None, initial_mitigations=None, open_questions_for_mrm=None):
    """
    Adds the Model Owner's qualitative risk narrative to the registration record.

    Args:
        model_record (dict): The existing model registration dictionary.
        owner_risk_narrative (str): The Model Owner's summary of the model's risk.
        known_limitations (list, optional): List of identified limitations of the model.
        initial_mitigations (list, optional): List of current or planned mitigation actions.
        open_questions_for_mrm (list, optional): Questions or areas for clarification for the MRM team.

    Returns:
        dict: The updated model registration dictionary.
    """
    if len(owner_risk_narrative) < 50: # Basic narrative length validation
        raise ValueError("Owner risk narrative must be at least 50 characters long for comprehensive assessment.")

    model_record.update({
        'owner_risk_narrative': owner_risk_narrative,
        'known_limitations': known_limitations if known_limitations is not None else [],
        'initial_mitigations': initial_mitigations if initial_mitigations is not None else [],
        'open_questions_for_mrm': open_questions_for_mrm if open_questions_for_mrm is not None else []
    })
    return model_record

# Alex adds the qualitative risk narrative
predictive_maintenance_model = add_owner_risk_narrative(
    predictive_maintenance_model,
    owner_risk_narrative="The Predictive Maintenance Model, while deployed in real-time, operates in an advisory capacity. Its primary function is to surface potential equipment anomalies for human review, reducing the direct impact of model errors. Data sensitivity is internal, focusing on machine telemetry. The 'Medium' criticality reflects potential operational downtime, not financial loss or regulatory non-compliance.",
    known_limitations=[
        "Performance may degrade with significant changes in machine types not seen during training.",
        "False positives could lead to unnecessary maintenance inspections, increasing operational costs.",
        "Relies on the quality and uptime of sensor data streams; data gaps could impact prediction accuracy."
    ],
    initial_mitigations=[
        "Regular monitoring of model performance metrics (precision, recall).",
        "Clear operational procedures for technicians to validate alerts before taking action.",
        "Redundancy in sensor data collection."
    ],
    open_questions_for_mrm=[
        "What are the specific performance thresholds for a Tier 3 operational model?",
        "Are there any specific data governance requirements for internal machine telemetry data?"
    ]
)

print(json.dumps(predictive_maintenance_model, indent=2))
```

### Explanation of Execution

Alex's detailed narrative provides invaluable context for the MRM team. It explains *why* the model's inherent risk factors were assessed the way they were and highlights practical considerations. For example, Alex notes the model's "advisory capacity," which implicitly reduces its overall risk impact despite a "Real-time" deployment. This qualitative input complements the quantitative score, offering a more nuanced and complete risk profile, in line with SR 11-7's guidance on understanding model capabilities and limitations (SR 11-7, Section III, Page 3). It also creates a structured artifact for further MRM review, fostering "effective challenge."

---

## 7. Finalizing and Exporting the Model Registration Packet

### Story + Context + Real-World Relevance

As the final step, Alex consolidates all the collected metadata, the calculated risk score and tier, and the risk narrative into a single, structured "Model Registration Packet." This artifact is the formal deliverable of the self-assessment process and will be submitted to TechCo's Model Risk Management (MRM) team. Exporting this comprehensive record ensures that all information is consistently captured and readily available for the next stages of the MRM lifecycle (e.g., formal tiering by the Second Line of Defense). This process directly supports SR 11-7's requirement for comprehensive model inventory and detailed documentation for auditability and governance (SR 11-7, Section VI, Page 20: "Banks should maintain a comprehensive set of information for models implemented for use...").

### Code cell (function definition + function execution)

```python
def export_model_registration_packet(model_data, output_filepath="model_registration_packet.json"):
    """
    Exports the complete model registration data, including self-assessment, to a JSON file.

    Args:
        model_data (dict): The complete model registration dictionary.
        output_filepath (str): The path to save the JSON file.
    """
    model_data['submitted_at'] = datetime.datetime.now().isoformat()
    model_data['status'] = 'Initial Self-Assessment Submitted'

    with open(output_filepath, 'w') as f:
        json.dump(model_data, f, indent=4)
    print(f"Model Registration Packet successfully exported to '{output_filepath}'")

# Define the output file path
output_file = f"model_registration_predictive_maintenance_{predictive_maintenance_model['version']}.json"

# Alex exports the completed registration packet
export_model_registration_packet(predictive_maintenance_model, output_filepath=output_file)

# Display the final packet structure
print("\n--- Final Model Registration Packet Content ---")
print(json.dumps(predictive_maintenance_model, indent=2))
```

### Explanation of Execution

Alex has successfully generated the complete Model Registration Packet as a JSON file. This file contains all the necessary metadata, the calculated initial risk score, the proposed preliminary tier, and the qualitative risk narrative. This artifact is a tangible representation of the Model Owner's proactive engagement with MRM requirements. It provides a standardized, machine-readable format for the handover to the MRM team (Second Line of Defense), facilitating their formal review and tier validation process. This systematic approach embodies the spirit of SR 11-7 by embedding risk considerations at the source, ensuring that model risks are understood and documented from the earliest stages of development and implementation.
