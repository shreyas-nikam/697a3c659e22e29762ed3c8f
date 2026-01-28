# QuLab: First Line - AI Model Registration & Inherent Risk Self-Assessment

## 📊 Project Title and Description

**QuLab: First Line - Model Owner's Initial Model Registration & Self-Assessment**

This Streamlit application serves as a simulated lab environment for **Model Owners** at a fictional financial institution, **Apex Financial Services**. Its primary purpose is to guide model owners through the critical initial steps of registering a new AI model into the enterprise model inventory and performing a conceptual self-assessment of its inherent risk.

The application is designed to illustrate and reinforce the principles outlined in **SR Letter 11-7** ("Guidance on Model Risk Management"), a key regulatory framework for financial institutions. It emphasizes the importance of robust model documentation, early risk identification, and proactive governance in embedding responsible AI practices from the earliest stages of the model lifecycle. By providing a structured interface for metadata input and rule-based risk scoring, the tool aims to ensure that potential model risks are identified, understood, and communicated effectively, forming the "first line of defense" in Model Risk Management (MRM).

## ✨ Features

This application offers a guided workflow with the following key features:

*   **Comprehensive Model Metadata Input**: Collects essential information about the AI model, including its name, business use, domain, type, deployment mode, owner team, stage, and region.
*   **Inherent Risk Factor Selection**: Allows the model owner to select critical characteristics that influence the model's inherent risk profile, such as Decision Criticality, Data Sensitivity, Automation Level, and Regulatory Materiality.
*   **Automated Inherent Risk Scoring**: Calculates a quantitative inherent risk score based on predefined rules and a scoring table, reflecting the impact of selected risk factors.
*   **Proposed Risk Tier Assignment**: Automatically assigns a preliminary risk tier (e.g., Low, Medium, High) based on the calculated inherent risk score and configurable thresholds.
*   **Interactive Risk Score Preview**: Visualizes the overall inherent risk score, proposed tier, and provides a detailed breakdown of how each risk factor contributed to the total score through tables and charts.
*   **SR 11-7 Contextual Guidance**: Integrates regulatory guidance and key principles from SR 11-7 directly into the application flow, highlighting the importance of each step in the MRM framework.
*   **Qualitative Risk Narrative Capture**: Provides text areas for the model owner to articulate their inherent risk narrative, proposed mitigations, and open questions, adding crucial qualitative context to the quantitative assessment.
*   **Export Consolidated Registration Artifact**: Generates a comprehensive JSON file containing all captured metadata, risk assessment details, and narratives, ready for integration into a centralized model inventory system.
*   **Session State Management**: Persists user inputs across different pages and browser refresh (within a session) for a smooth user experience.

## 🚀 Getting Started

Follow these instructions to set up and run the Streamlit application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quolab-first-line-mrm.git
    cd quolab-first-line-mrm
    ```
    *(Note: Replace `your-username/quolab-first-line-mrm` with the actual repository URL if available, otherwise just use a generic local directory name.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install the required dependencies:**
    Create a `requirements.txt` file in the root directory of your project with the following content:
    ```
    streamlit
    pandas
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

Once the dependencies are installed, you can run the Streamlit application.

1.  **Ensure you are in the project's root directory** (`quolab-first-line-mrm`) and your virtual environment is activated.

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    *(Assuming your main Streamlit script is named `app.py`)*

3.  **Access the application:**
    Your web browser should automatically open to the application's local URL (usually `http://localhost:8501`). If not, copy and paste the URL displayed in your terminal.

### Basic Usage Instructions:

*   **Page 1: Model Registration**:
    *   Fill in all the required model details (marked with `*`).
    *   Carefully select the "Inherent Risk Factors ⚡" based on your model's characteristics. These selections directly influence the calculated risk score.
    *   Click "Register Model & Assess Risk" to proceed.
*   **Page 2: Risk Score Preview**:
    *   Review the calculated "Inherent Risk Score" and "Proposed Risk Tier".
    *   Examine the "Scoring Methodology" and "Score Breakdown by Factor" to understand how the score was derived.
*   **Page 3: Narrative & Export**:
    *   Provide your "Owner's Inherent Risk Narrative" (minimum 50 characters is required for export).
    *   Optionally add "Proposed Mitigations" and "Open Questions / Follow-ups".
    *   Review the JSON export preview.
    *   Click "Download Model Registration JSON" to save the complete artifact. The download button will be enabled once a model is registered and the narrative meets the minimum length requirement.

## 📁 Project Structure

```
.
├── app.py                     # Main Streamlit application file
├── source.py                  # Contains core logic for risk scoring and metadata registration
├── requirements.txt           # Lists Python dependencies
└── README.md                  # This README file
```

### `app.py`
This is the main entry point for the Streamlit application. It handles the UI layout, user input, navigation, session state management, and calls functions from `source.py` for business logic.

### `source.py`
This file contains the core Python functions and data definitions used by the application, specifically:
*   `RISK_SCORING_TABLE`: A dictionary defining points for each value of inherent risk factors.
*   `TIER_THRESHOLDS`: A dictionary defining score ranges for different risk tiers.
*   `SCORING_VERSION`: Version identifier for the scoring methodology.
*   `register_model_metadata(model_details)`: Generates a unique Model ID and adds audit fields to the model details.
*   `calculate_inherent_risk(registered_model_output, scoring_table, tier_thresholds, scoring_version)`: Calculates the total inherent risk score, assigns a tier, and provides a breakdown.

## 💻 Technology Stack

*   **Python**: The core programming language.
*   **Streamlit**: For building interactive web applications with pure Python.
*   **Pandas**: Used for data manipulation and display (e.g., scoring tables, score breakdown).
*   **JSON**: For data serialization and export of the model registration artifact.
*   **uuid & datetime**: Python built-in modules for generating unique IDs and timestamps.

## 🤝 Contributing

This project is primarily a lab demonstration. However, if you have suggestions for improvements or encounter issues, please feel free to:

1.  **Fork** the repository.
2.  **Create a new branch** (`git checkout -b feature/AmazingFeature` or `fix/BugFix`).
3.  **Make your changes**.
4.  **Commit your changes** (`git commit -m 'Add some AmazingFeature'`).
5.  **Push to the branch** (`git push origin feature/AmazingFeature`).
6.  **Open a Pull Request**.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details (if applicable, otherwise state "No specific license, for educational purposes only").

*(Note: For a real project, you would include an actual `LICENSE` file at the root of your repository.)*

## 📧 Contact

For questions or inquiries regarding this QuLab project, please contact:

*   **QuantUniversity:** [https://www.quantuniversity.com](https://www.quantuniversity.com)
*   **Email:** info@quantuniversity.com

---
*Developed as part of the QuantUniversity Lab Series.*


## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@qusandbox.com](mailto:info@qusandbox.com)
