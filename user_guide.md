id: 697a3c659e22e29762ed3c8f_user_guide
summary: First Line - Model Owner's Initial Model Registration & Self-Assessment User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Registering and Assessing AI Model Risk

## 1) Understanding Model Registration and Initial Self-Assessment
Duration: 10:00

Welcome to QuLab's First Line AI Model Registration & Self-Assessment application! This codelab will guide you through the process of formally registering a new AI model and performing an initial assessment of its inherent risk within Apex Financial Services.

In today's financial landscape, the responsible deployment of Artificial Intelligence (AI) models is paramount. Regulatory guidance, such as the **SR Letter 11-7**, emphasizes the critical importance of robust Model Risk Management (MRM) frameworks. As a **System / Model Owner**, your role in this initial registration and self-assessment phase is not merely administrative; it's a foundational step in ensuring compliance, transparency, and proactive risk mitigation throughout the model's lifecycle.

This application simplifies the process of:
*   **Model Documentation:** Capturing essential metadata, forming the "comprehensive set of information for models implemented for use" as mandated by SR 11-7 (Page 20).
*   **Early Risk Thinking:** Identifying and assessing potential risks at the earliest stage, which helps embed risk considerations at the source, saving time and reducing rework later.
*   **Model Inventory Contribution:** Structured data from this assessment feeds into the firm-wide model inventory, crucial for enterprise-level oversight.

The concepts you'll engage with directly address key SR 11-7 principles, including:
*   **Model Documentation:** Ensuring transparency and auditability.
*   **Early Risk Thinking:** Proactive management of potential adverse consequences.
*   **Owner Responsibilities:** Your accountability for accurate information and initial risk assessment.

<aside class="positive">
<b>Pro Tip:</b> Think of this application as your first line of defense in managing model risk. Accurate and thoughtful inputs here set the stage for a smooth and compliant model lifecycle!
</aside>



### Navigating the Application

The application is structured into three main pages, accessible via the sidebar on the left:
1.  **Model Registration:** Where you input all model details and risk factors.
2.  **Risk Score Preview:** Where you see the calculated inherent risk and its breakdown.
3.  **Narrative & Export:** Where you add qualitative context and export the complete record.

You can move between these pages using the dropdown in the sidebar, or the application will automatically advance you after completing certain steps.

### 1. Register Your AI Model: Metadata Input

Your first task is to provide comprehensive metadata for your model. This detailed documentation is fundamental, as it underpins all subsequent MRM activities. Without adequate documentation, assessing and managing model risk becomes ineffective.

Focus on defining your model's attributes in the form provided. Pay special attention to the fields marked with `*` and those under **"Inherent Risk Factors ⚡"**, as these selections directly influence the model's inherent risk score.

#### Model Core Details

Fill out the following sections:

*   **Model Name:** Provide a clear, descriptive name for your model, e.g., "Predictive Maintenance Model v2.1".
*   **Domain:** Select the primary business area this model operates within (e.g., 'Operations Efficiency', 'Credit Risk').
*   **Model Type:** Identify the technical nature of the model (e.g., 'ML classifier (time-series)', 'Neural Network').
*   **Deployment Mode:** Specify how the model operates in production (e.g., 'Real-time', 'Batch').
*   **Owner Team (Optional):** The team responsible for the model.
*   **Business Use & Objective:** Crucially, describe what the model does and why it's being used. This context is vital for understanding its purpose and potential impact.
*   **Model Stage (Optional):** Indicate its current stage in the development or deployment lifecycle.
*   **Deployment Region (Optional):** Where the model is intended to be deployed geographically.

#### Inherent Risk Factors ⚡

These factors are critical for the automated risk assessment. Select the option that best describes your model for each factor. Each selection has an associated risk "weight" that contributes to the overall score.

*   **Decision Criticality:** How significant are the decisions made by or supported by this model? What is the potential impact of an incorrect output?
*   **Data Sensitivity:** What kind of data does the model process? Does it involve personally identifiable information (PII), confidential business data, or highly sensitive financial information?
*   **Automation Level:** To what extent are the model's decisions automated and acted upon without human intervention? Higher automation often implies higher inherent risk.
*   **Regulatory Materiality:** Is the business area or decision supported by this model subject to significant regulatory scrutiny (e.g., credit decisions, fraud reporting)?

<aside class="negative">
<b>Warning:</b> Ensure all required fields (marked with `*`) are completed. The application will prevent submission and show an error if any mandatory information is missing.
</aside>

Once all details are entered, click the **"Register Model & Assess Risk"** button. The application will validate your inputs, calculate an initial inherent risk score, and then automatically navigate you to the next page.

## 2) Understanding Your Inherent Risk Score
Duration: 08:00

After successfully registering your model, you'll land on the "Risk Score Preview" page. This section is dedicated to presenting the initial inherent risk assessment based on the characteristics you provided. This step is crucial for "assessing the magnitude" of model risk, a core activity outlined in SR 11-7 (Page 4). Understanding this score helps determine the appropriate level of scrutiny and governance required for your model.

Apex Financial Services uses a predefined, rule-based system to calculate an initial inherent risk score and assign a preliminary risk tier. This system systematically quantifies model risk by considering factors like model complexity, data sensitivity, and potential impact.



### 2. Your Model's Inherent Risk Assessment Results

At the top of the page, you'll see two key metrics:

*   **Inherent Risk Score:** This is a numerical value representing the total calculated risk of your model *before* any mitigating controls are put in place. A higher score indicates higher inherent risk.
*   **Proposed Risk Tier:** Based on the inherent risk score, your model is categorized into a preliminary risk tier (e.g., 'Low', 'Medium', 'High'). This tier often dictates the level of oversight and validation required.

<aside class="positive">
<b>Context:</b> An "inherent risk" score reflects the risk posed by the model itself, given its characteristics and use, in the absence of any mitigating controls. It answers the question: "How risky is this model if we don't do anything to manage that risk?"
</aside>

### Scoring Methodology

Our framework assigns points to specific categorical values for each risk factor you selected during registration. The total inherent risk score is then calculated as the sum of points from each factor.

Mathematically, this can be expressed as:

$$ S_{total} = \sum_{f \in \text{Factors}} P(V_f) $$

Where:
*   $S_{total}$ is the total inherent risk score.
*   $f$ represents a risk factor (e.g., `decision_criticality`).
*   $P(V_f)$ is the points assigned to the chosen value $V_f$ for that factor (e.g., 'Very High' for `decision_criticality` might yield 5 points).

The preliminary risk tier is then determined by comparing this $S_{total}$ against predefined thresholds.

#### Risk Factor Scoring Table

Review the `Risk Factor Scoring Table` to see how points are assigned to each possible selection for `Decision Criticality`, `Data Sensitivity`, `Automation Level`, and `Regulatory Materiality`. This table provides full transparency on how each of your choices contributed to the final score.

#### Proposed Risk Tier Thresholds

The `Proposed Risk Tier Thresholds` table illustrates the score ranges that define each risk tier (e.g., 'Low' might be 0-5 points, 'Medium' 6-10 points, etc.). This helps you understand why your model received its particular tier.

### Score Breakdown by Factor

This section provides a detailed breakdown of how each individual risk factor contributed to your model's overall inherent risk score.

*   **Table:** A table lists each `Factor`, the `Value` you selected for it, and the `Points` assigned.
*   **Bar Chart:** A visual representation (bar chart) shows the `Points Contribution` from each factor, making it easy to see which factors contribute most to your model's inherent risk.

This breakdown is invaluable for understanding the drivers of your model's risk and for identifying areas that might require specific attention or mitigation strategies.

## 3) Crafting the Risk Narrative & Exporting
Duration: 10:00

The final step in the initial model registration and self-assessment process is to provide qualitative context and export the complete model record. While structured data and a calculated score are essential, a clear narrative is equally critical for effective Model Risk Management. It enriches the structured data, explains assumptions, outlines potential mitigations, and raises any open questions, fulfilling SR 11-7's requirement for comprehensive documentation.

SR 11-7 Section VI ("Governance, Policies, and Controls") emphasizes that model documentation should be "sufficiently detailed so that parties unfamiliar with a model can understand how the model operates, its limitations, and its key assumptions." Your narrative is key to achieving this by adding qualitative depth to the quantitative assessment.



### 3. Risk Narrative & Additional Context

You will find three text areas to provide this crucial qualitative information:

*   **Owner's Inherent Risk Narrative (Required):** This is where you, as the Model Owner, provide a narrative summary of your initial inherent risk assessment. Explain *why* you made certain selections for the risk factors, discuss any specific considerations or assumptions, and elaborate on your understanding of the model's core risks. This field requires a minimum length (50 characters) to ensure adequate detail.
*   **Proposed Mitigations (Optional):** If you already have ideas for how to reduce or manage the identified inherent risks (e.g., "Implement stricter data validation checks," "Require human review for high-risk predictions"), list them here.
*   **Open Questions / Follow-ups (Optional):** Use this space to note any uncertainties, areas requiring further investigation, or specific follow-up actions that need to be taken regarding the model's risk profile.

<aside class="negative">
<b>Warning:</b> The "Owner's Inherent Risk Narrative" is a mandatory field and must meet the minimum character length. The download functionality will be disabled until this requirement is met.
</aside>

### 4. Export Model Registration Artifact

This section allows you to preview and export the complete model registration record. This includes all the metadata you entered, the inherent risk assessment results, and the narratives you just provided, consolidated into a single JSON file. This artifact is designed for easy ingestion into Apex Financial Services' centralized model inventory.

#### JSON Export Preview

You will see a live preview of the JSON file that will be generated. This JSON object contains all the structured and unstructured data related to your model's registration and self-assessment. Review it to ensure all information is present and accurate.

#### Download Model Registration JSON

Once you have registered your model and provided a sufficiently detailed inherent risk narrative, the **"Download Model Registration JSON"** button will become active. Clicking this button will download the complete JSON artifact to your local machine.

<aside class="positive">
<b>Best Practice:</b> Downloading this JSON file completes your initial registration and self-assessment process. This file serves as the formal record for your model and should be submitted to the central Model Risk Management team for review and record-keeping.
</aside>

Congratulations! You have successfully registered your AI model, performed an initial inherent risk self-assessment, and generated the necessary documentation. This proactive engagement is a vital contribution to Apex Financial Services' robust Model Risk Management framework and promotes a culture of responsible AI deployment.
