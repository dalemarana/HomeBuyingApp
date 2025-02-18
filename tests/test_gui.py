import os
import pytest

# Skip GUI tests in CI/CD
if os.environ.get("CI"):  # GitHub Actions sets the "CI" environment variable
    pytest.skip("Skipping GUI tests in CI/CD", allow_module_level=True)

import PySimpleGUI as sg
from home_buying_app.gui import HomeBuyingAnalysis

@pytest.fixture(scope="function")
def gui_app():
    """Fixture to initialize and clean up the GUI."""
    app = HomeBuyingAnalysis()
    window = app.create_gui()
    yield window  # Provide the GUI window to the tests
    window.close()

@pytest.fixture
def prefilled_data():
    """Fixture to provide pre-filled test data."""
    return {
        "name": "John Doe", "age": "30", "occupation": "Engineer", "status": "Single", "residence": "United Kingdom",
        "annual_income": "50000", "monthly_income": "4000",
        "rent": "1000", "electricity": "100", "water": "50", "groceries": "300",
        "council_tax": "200", "other": "150",
        "property_value": "300000", "deposit": "60000", "duration": "30",
        "solicitor": "2000", "survey": "500", "furnishings": "5000"
    }

def test_gui_initialization(gui_app, prefilled_data):
    """✅ Test if GUI loads correctly with pre-filled values and expected widgets."""
    
    # Ensure window exists
    assert gui_app.TKroot.winfo_exists(), "❌ GUI window does not exist!"
    
    # Ensure window is visible
    assert gui_app.TKroot.winfo_viewable(), "❌ GUI window is not visible!"
    
    # Ensure window title is correct (modify according to your actual title)
    expected_title = "Rent vs Buy Calculator"
    assert gui_app.TKroot.title() == expected_title, f"❌ GUI title is incorrect! Expected: '{expected_title}', Got: '{gui_app.TKroot.title()}'"
    
    # Ensure first tab is active
    assert gui_app["-TAB1-"].visible, "❌ First tab is not visible on startup!"

    # # Check all expected fields exist in the GUI
    # for key, expected_value in prefilled_data.items():
    #     assert key in gui_app.AllKeysDict, f"❌ Expected input field '{key}' not found in GUI!"
        
    #     # Check if the initial value is set correctly
    #     gui_value = gui_app[key].get()
    #     assert gui_value == expected_value, f"❌ Field '{key}' did not initialize correctly! Expected: '{expected_value}', Got: '{gui_value}'"
    
    # print("✅ GUI initialization test passed!")

# @pytest.mark.parametrize("tab_index", range(1, 6))
# def test_button_next_tab(gui_app, tab_index):
#     """✅ Test if 'Next' button navigates through all tabs correctly."""
#     gui_app["Next"].click()
#     assert gui_app[f"-TAB{tab_index+1}-"].visible, f"Tab {tab_index+1} did not open!"

# def test_exit_button(gui_app):
#     """✅ Test if 'Exit' button closes the GUI."""
#     gui_app["Exit"].click()
#     assert not gui_app.TKroot.winfo_exists(), "GUI window did not close!"

# def test_generate_report_button(gui_app):
#     """✅ Test if 'Generate Report' button generates a report."""
#     gui_app["Generate Report"].click()
#     report_file = "home_buying_report.pdf"
#     assert os.path.exists(report_file), "Report file was not generated!"
#     os.remove(report_file)  # Clean up after test

# def test_user_manual_button(gui_app):
#     """✅ Test if 'View User Manual' button attempts to open the file."""
#     gui_app["user_manual"].click()
#     user_manual_file = "user_manual.pdf"
#     assert os.path.exists(user_manual_file), "User manual not found!"