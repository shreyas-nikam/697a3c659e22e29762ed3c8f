
from streamlit.testing.v1 import AppTest
import json

# Mock the source.py functions for testing purposes
# In a real test setup, you might have a dedicated mock file or use unittest.mock.patch
# For this example, we'll define simple mocks that return expected structures.

RISK_SCORING_TABLE = {
    'decision_criticality': {
        'Low': {'points': 1},
        'Medium': {'points': 2},
        'High': {'points': 3}
    },
    'data_sensitivity': {
        'Public': {'points': 1},
        'Confidential': {'points': 2},
        'Restricted': {'points': 3}
    },
    'automation_level': {
        'Manual': {'points': 1},
        'Semi-Automated': {'points': 2},
        'Fully Automated': {'points': 3}
    },
    'regulatory_materiality': {
        'Low': {'points': 1},
        'Medium': {'points': 2},
        'High': {'points': 3}
    }
}

TIER_THRESHOLDS = {
    'Low': {'min_score': 4, 'max_score': 7, 'description': 'Minimal oversight needed'},
    'Medium': {'min_score': 8, 'max_score': 10, 'description': 'Standard oversight needed'},
    'High': {'min_score': 11, 'max_score': 12, 'description': 'Intensive oversight needed'}
}

SCORING_VERSION = "1.0"

def register_model_metadata(raw_details):
    # Simulate generating model_id and audit fields
    model_id = str(raw_details.get('model_id', 'test_id_123'))
    registered_at = "2026-01-28T18:30:00Z" # Fixed for consistent testing
    return {
        **raw_details,
        'model_id': model_id,
        'registered_at': registered_at
    }

def calculate_inherent_risk(model_details, risk_table, tier_thresholds, scoring_version):
    total_score = 0
    score_breakdown = {}
    
    factors = ['decision_criticality', 'data_sensitivity', 'automation_level', 'regulatory_materiality']
    for factor in factors:
        value = model_details.get(factor)
        if value and value in risk_table[factor]:
            points = risk_table[factor][value]['points']
            total_score += points
            score_breakdown[factor] = {'value': value, 'points': points}
            
    proposed_tier = "Unknown"
    proposed_tier_description = ""
    for tier, thresholds in tier_thresholds.items():
        if thresholds['min_score'] <= total_score <= thresholds['max_score']:
            proposed_tier = tier
            proposed_tier_description = thresholds['description']
            break
            
    return {
        'inherent_risk_score': total_score,
        'proposed_risk_tier': proposed_tier,
        'proposed_tier_description': proposed_tier_description,
        'score_breakdown': score_breakdown,
        'scoring_version': scoring_version
    }


def test_initial_app_load_and_default_page():
    at = AppTest.from_file("app.py").run()
    assert at.session_state['current_page'] == '1) Model Registration', "Should start on Model Registration page"
    assert "📊 AI Model Registration" in at.markdown[1].value, "Page 1 title should be present"
    assert not at.session_state['model_registered'], "model_registered should be false initially"
    assert at.selectbox[0].value == '1) Model Registration', "Sidebar selectbox should show correct page"


def test_model_registration_success():
    at = AppTest.from_file("app.py").run()

    # Fill out the form
    at.text_input[0].set_value("Test Model v1.0").run()  # Model Name
    at.selectbox[1].set_value("Operations Efficiency").run()  # Domain
    at.selectbox[2].set_value("ML classifier (time-series)").run()  # Model Type
    at.selectbox[3].set_value("Real-time").run() # Deployment Mode
    # Owner Team (optional) - leave default or set
    at.text_input[1].set_value("Test Team").run()

    at.text_area[0].set_value("This model predicts equipment failures.").run()  # Business Use
    at.selectbox[4].set_value("Production").run()  # Model Stage (optional)
    at.text_input[2].set_value("North America").run()  # Deployment Region (optional)

    # Inherent Risk Factors
    at.selectbox[5].set_value("High").run()  # Decision Criticality (points: 3)
    at.selectbox[6].set_value("Restricted").run()  # Data Sensitivity (points: 3)
    at.selectbox[7].set_value("Fully Automated").run()  # Automation Level (points: 3)
    at.selectbox[8].set_value("High").run()  # Regulatory Materiality (points: 3)

    # Submit the form
    at.form[0].submit().run()

    # Assertions after successful submission
    assert at.success[0].value == "Model registered and risk assessed successfully! Proceed to 'Risk Score Preview'.", "Success message should be displayed"
    assert at.session_state['model_registered'], "model_registered should be True"
    assert at.session_state['current_page'] == '2) Risk Score Preview', "Should navigate to Risk Score Preview page"
    assert at.session_state['model_details']['model_name'] == "Test Model v1.0", "Model name should be stored in session state"
    assert at.session_state['model_details']['inherent_risk_score'] == 12, "Inherent risk score should be calculated correctly (3+3+3+3)"
    assert at.session_state['model_details']['proposed_risk_tier'] == 'High', "Proposed risk tier should be High"
    assert 'model_id' in at.session_state['model_details'], "Model ID should be generated"


def test_model_registration_missing_fields_validation():
    at = AppTest.from_file("app.py").run()

    # Submit the form without filling any required fields
    at.form[0].submit().run()

    # Assertions for missing fields
    assert "Please fill in all required fields (marked with '*') " in at.error[0].value, "Error message for missing fields should appear"
    assert not at.session_state['model_registered'], "Model should not be registered if fields are missing"
    assert at.session_state['current_page'] == '1) Model Registration', "Should remain on Model Registration page"


def test_navigation_to_risk_score_preview_page_without_registration():
    at = AppTest.from_file("app.py").run()

    # Manually navigate to Risk Score Preview without registering
    at.selectbox[0].set_value("2) Risk Score Preview").run()

    assert at.session_state['current_page'] == '2) Risk Score Preview', "Should navigate to Risk Score Preview page"
    assert "Please complete the 'Model Registration' page first" in at.warning[0].value, "Warning should be displayed"
    assert not at.session_state['model_details'], "Model details should be empty"


def test_risk_score_preview_page_content_after_registration():
    at = AppTest.from_file("app.py")
    # Simulate a registered model in session state
    at.session_state['model_registered'] = True
    at.session_state['model_details'] = {
        'model_name': 'Test Model X',
        'business_use': 'Predict customer churn',
        'domain': 'Customer Segmentation',
        'model_type': 'ML classifier (time-series)',
        'decision_criticality': 'Medium',
        'data_sensitivity': 'Confidential',
        'automation_level': 'Semi-Automated',
        'deployment_mode': 'Batch',
        'regulatory_materiality': 'Low',
        'owner_team': 'Data Science',
        'model_stage': 'Development',
        'deployment_region': 'EMEA',
        'model_id': 'test-model-x-123',
        'registered_at': '2023-01-01T12:00:00Z',
        'inherent_risk_score': 7, # 2+2+2+1
        'proposed_risk_tier': 'Low',
        'proposed_tier_description': 'Minimal oversight needed',
        'score_breakdown': {
            'decision_criticality': {'value': 'Medium', 'points': 2},
            'data_sensitivity': {'value': 'Confidential', 'points': 2},
            'automation_level': {'value': 'Semi-Automated', 'points': 2},
            'regulatory_materiality': {'value': 'Low', 'points': 1}
        },
        'scoring_version': '1.0'
    }
    at.session_state['current_page'] = '2) Risk Score Preview'
    at.run()

    assert at.markdown[1].value == "# 🔍 Inherent Risk Score Preview", "Page title should be correct"
    assert at.metric[0].value == 7, "Inherent Risk Score metric should display correct value"
    assert at.metric[1].value == "Low - Minimal oversight needed", "Proposed Risk Tier metric should display correct value and description"
    assert "Scoring Methodology" in at.markdown[3].value, "Scoring methodology section should be present"
    assert "Risk Factor Scoring Table (Version: `1.0`)" in at.markdown[6].value, "Scoring table header should include version"
    assert at.dataframe[0].value is not None, "Risk factor scoring table should be displayed"
    assert at.dataframe[1].value is not None, "Proposed risk tier thresholds table should be displayed"
    assert "Score Breakdown by Factor" in at.markdown[9].value, "Score breakdown section should be present"
    assert at.dataframe[2].value is not None, "Score breakdown dataframe should be displayed"
    assert at.bar_chart[0].value is not None, "Bar chart of points contribution should be displayed"


def test_narrative_export_page_without_registration():
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("3) Narrative & Export").run()

    assert "Please complete the 'Model Registration' page first." in at.warning[0].value, "Warning should be displayed"
    assert at.button[0].disabled, "Download button should be disabled without registration"


def test_narrative_export_page_with_registration_and_narrative_validation():
    at = AppTest.from_file("app.py")
    # Simulate a registered model in session state
    at.session_state['model_registered'] = True
    at.session_state['model_details'] = {
        'model_name': 'Test Model Y',
        'business_use': 'Fraud detection',
        'domain': 'Fraud Detection',
        'model_type': 'Regression',
        'decision_criticality': 'High',
        'data_sensitivity': 'Restricted',
        'automation_level': 'Fully Automated',
        'deployment_mode': 'Real-time',
        'regulatory_materiality': 'High',
        'owner_team': 'Risk Ops',
        'model_id': 'test-model-y-456',
        'registered_at': '2023-02-01T10:00:00Z',
        'inherent_risk_score': 12,
        'proposed_risk_tier': 'High',
        'proposed_tier_description': 'Intensive oversight needed',
        'score_breakdown': {
            'decision_criticality': {'value': 'High', 'points': 3},
            'data_sensitivity': {'value': 'Restricted', 'points': 3},
            'automation_level': {'value': 'Fully Automated', 'points': 3},
            'regulatory_materiality': {'value': 'High', 'points': 3}
        },
        'scoring_version': '1.0'
    }
    at.session_state['current_page'] = '3) Narrative & Export'
    at.run()

    assert at.text_area[0].value == "", "Narrative text area should be empty initially"
    assert at.button[0].disabled, "Download button should be disabled due to empty narrative"
    assert "Owner's Inherent Risk Narrative must be at least 50 characters long." in at.warning[0].value, "Narrative length warning should appear"

    # Input a short narrative
    at.text_area[0].set_value("Too short.").run()
    assert at.warning[0].value is not None, "Warning should still be present for short narrative"
    assert at.button[0].disabled, "Download button should still be disabled"

    # Input a sufficiently long narrative
    long_narrative = "This is a sufficiently long narrative to meet the minimum character requirement of fifty characters."
    at.text_area[0].set_value(long_narrative).run()
    assert at.warning[0].empty, "Warning should disappear for valid narrative length"
    assert not at.button[0].disabled, "Download button should be enabled"
    
    # Fill in optional fields
    mitigations = "Proposed mitigations: Enhanced monitoring, regular model retraining."
    open_questions = "Open questions: Impact of new data sources, performance in extreme market conditions."
    at.text_area[1].set_value(mitigations).run()
    at.text_area[2].set_value(open_questions).run()

    # Verify export artifact content
    expected_export_data = {
        **at.session_state['model_details'],
        'owner_risk_narrative': long_narrative,
        'mitigations_proposed': mitigations,
        'open_questions': open_questions,
        'export_format_version': 'lab1_export_v1'
    }
    assert at.session_state['export_artifact'] == expected_export_data, "Export artifact should contain all details and narrative"
    assert json.loads(at.json[0].value) == expected_export_data, "JSON preview should match export artifact"
    assert at.button[0].attrs[0].kwargs['file_name'] == "lab1_test_model_y.json", "Download button filename should be correct"


def test_navigation_sidebar():
    at = AppTest.from_file("app.py").run()

    # Navigate from Page 1 to Page 2
    at.selectbox[0].set_value("2) Risk Score Preview").run()
    assert at.session_state['current_page'] == '2) Risk Score Preview'
    assert "🔍 Inherent Risk Score Preview" in at.markdown[1].value

    # Navigate from Page 2 to Page 3
    at.selectbox[0].set_value("3) Narrative & Export").run()
    assert at.session_state['current_page'] == '3) Narrative & Export'
    assert "✍️ Narrative & Export Model Registration" in at.markdown[1].value

    # Navigate from Page 3 to Page 1
    at.selectbox[0].set_value("1) Model Registration").run()
    assert at.session_state['current_page'] == '1) Model Registration'
    assert "📊 AI Model Registration" in at.markdown[1].value
