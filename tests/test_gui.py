import unittest
import sys
import os
from unittest.mock import patch, MagicMock

import PySimpleGUI as sg
# Add the root folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add the home_buying_app folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'home_buying_app')))

from home_buying_app.gui import HomeBuyingAnalysis

CLIENT_DETAILS =  {
        "name": "John Doe",
        "age": "30",
        "occupation": "Engineer",
        "status": "Single",
        "residence": "United Kingdom",
    }

FINANCIAL_DETAILS = {
        "annual_income": "50000",
        "monthly_income": "4000"
    }

EXPENSES = {
        "rent": "1000",
        "electricity": "100",
        "water": "50",
        "groceries": "300",
        "council_tax": "200",
        "other": "150"
    }

PROPERTY_DETAILS = {
        "property_value": "300000",
        "deposit": "60000",
        "duration": "30",
        "solicitor": "2000",
        "survey": "500",
        "furnishings": "5000"
    }


class TestHomeBuyingAnalysisGUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all tests. Useful for setup tasks."""
        cls.app = HomeBuyingAnalysis() # Create an instance of the class

    def setUp(self):
        """Runs before each test. Creates a new GUI instance for each test."""

        # self.app.client_details = CLIENT_DETAILS
        # self.app.financial_details = FINANCIAL_DETAILS
        # self.app.expenses = EXPENSES
        # self.app.property_details = PROPERTY_DETAILS

        self.test_data = {
            "name": "John Doe", "age": "30", "occupation": "Engineer", "status": "Single", "residence": "USA",
            "annual_income": "50000", "monthly_income": "4000",
            "rent": "1000", "electricity": "100", "water": "50", "groceries": "300",
            "council_tax": "200", "other": "150",
            "property_value": "300000", "deposit": "60000", "duration": "30",
            "solicitor": "2000", "survey": "500", "furnishings": "5000"
        }

        # 🔹 Now create GUI after pre-population
        self.window = self.app.create_gui()  
    
        # 🔹 Ensure the window is properly created before proceeding
        if self.window is None:
            self.fail("GUI window was not created!")

        # ✅ Update fields only if window exists
        if self.window.TKroot.winfo_exists():
            for key, value in self.test_data.items():
                if key in self.window.AllKeysDict:
                    self.window[key].update(value)  # ✅ Update GUI fields only if window exists

    def tearDown(self):
        """Runs after each test. Closes the window to free resources."""
        if self.window:
            self.window.close()

    def test_gui_initialization(self):
        """✅ Test if GUI loads correctly with pre-filled values."""
        
        self.assertTrue(self.window.TKroot.winfo_exists(), "GUI window does not exist!")

        # 🔹 Check input fields using a loop
        for key, expected_value in self.test_data.items():
            with self.subTest(field=key):
                self.assertEqual(self.window[key].get(), expected_value)


    # def test_button_next_tab(self):
    #     """✅ Test if 'Next' button navigates tabs correctly."""
        
    #     for i in range(1, 6):  # Loop through tabs 1 to 5
    #         next_event = "Next"
    #         self.window[next_event].click()
    #         with self.subTest(tab=f"TAB{i}"):
    #             print(f"-TAB{i}-")
    #             self.assertTrue(self.window[f"-TAB{i}-"].visible, f"Tab {i} did not open!")

    # def test_exit_button(self):
    #     """✅ Test if 'Exit' button closes the GUI."""
        
    #     self.window["Exit"].click()
    #     self.assertFalse(self.window.TKroot.winfo_exists(), "GUI window did not close!")

    def test_generate_report_button(self):
        """✅ Test if 'Generate Report' button works correctly."""
        
        self.window["Generate Report"].click()
        
        # 🔹 Check if report file exists
        report_file = "home_buying_report.pdf"
        self.assertTrue(os.path.exists(report_file), "Report file was not generated!")

        # 🔹 Clean up: remove test report
        os.remove(report_file)

    # def test_user_manual_button(self):
    #     """✅ Test if 'View User Manual' button tries to open the file."""
        
    #     # Simulate button click
    #     self.window["user_manual"].click()

    #     # Check if file exists (mocking os.startfile behavior)
    #     user_manual_file = "user_manual.pdf"
    #     self.assertTrue(os.path.exists(user_manual_file), "User manual not found!")


if __name__ == '__main__':
    unittest.main()
