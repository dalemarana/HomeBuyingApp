import os
import pytest


import numpy as np
import matplotlib.pyplot as plt
# Skip output tests in CI/CD
if os.environ.get("CI"):  # GitHub Actions sets the "CI" environment variable
    pytest.skip("Skipping GUI tests in CI/CD", allow_module_level=True)
from output import generate_conclusion, generate_conclusion_graphs, comma_formatter

@pytest.fixture
def sample_data():
    """Fixture providing sample input data for tests."""
    return {
        "user_details": [
            {"currency": "GBP"}
        ],
        "expense_cost_analysis": [{
            "remaining_income_mortgage": 99769.020300508,
            "remaining_income_mortgage_pv": 1146962.8266962562,
            "remaining_income_rent_pv": 985403.4782878414
        }],
        "non_recoverable_costs": [{
            "homeownership_costs_pv": 292876.1914671146,
            "renting_costs_pv": 664697.7138520329,
            "nonrecoverable_cost_difference": -371821.5223849183
        }],
        "opportunity_costs": [{
            "home_equity_pv": 322159.3636797702,
            "stock_investment_pv": 291713.1672005757,
            "opportunity_cost_difference": 30446.196479194507
        }]
    }

@pytest.fixture
def sample_conclusion_data():
    """Fixture providing sample conclusion data for the graph."""
    return {
        "Expense Analysis": [985403.4782878414, 1146962.8266962562],
        "Non-Recoverable Costs": [664697.7138520329, 292876.1914671146],
        "Opportunity Costs": [291713.1672005757, 322159.3636797702]
    }

def test_generate_conclusion(sample_data):
    """Test the generate_conclusion function."""
    result = generate_conclusion(sample_data)

    assert "Expense Analysis:" in result
    assert "Homeownership provides better spending space with accummulated present value spending space difference of GBP 161,559.35." in result
    assert "Non-Recoverable Costs:" in result
    assert "Homeownership is more cost-effective over the analysis period, with a present value savings of GBP 371,821.52." in result
    assert "Opportunity Costs:" in result
    assert "Homeownership equity growth outperforms stock investments, with a present value advantage of GBP 30,446.20." in result
    assert "Recommendation:" in result


def test_generate_conclusion_graphs(sample_data, sample_conclusion_data, tmp_path):
    """Test the generate_conclusion_graphs function."""
    summary_graph_path = tmp_path / "summary_graph.png"

    plt.savefig = lambda *args, **kwargs: summary_graph_path.touch()  # Mock savefig

    result_path = generate_conclusion_graphs(sample_data, sample_conclusion_data)

    assert result_path is not None
    assert summary_graph_path.exists()  # Ensure the file was "saved"

# def test_comma_formatter():
#     """Test the comma_formatter function."""
#     assert comma_formatter(161559.35, 2) == "161,559.35"
#     assert comma_formatter(371821.52, 2) == "371,821.52"
#     assert comma_formatter(30446.196479194507, 2) == "30,446.20"
#     assert comma_formatter(-5000, 0) == "-5,000"