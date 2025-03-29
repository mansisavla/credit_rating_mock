import unittest
import json
from credit_rating import calculate_credit_rating

class TestCreditRating(unittest.TestCase):
    def test_valid_mortgages(self):
        """Test valid mortgages with different attributes."""
        data = [
            {
                "credit_score": 750,
                "loan_amount": 200000,
                "property_value": 250000,
                "annual_income": 60000,
                "debt_amount": 20000,
                "loan_type": "fixed",
                "property_type": "house"
            },
            {
                "credit_score": 680,
                "loan_amount": 150000,
                "property_value": 175000,
                "annual_income": 45000,
                "debt_amount": 10000,
                "loan_type": "adjustable",
                "property_type": "condo"
            }
        ]
        payload = json.dumps(data)
        rating = calculate_credit_rating(payload)
        self.assertIn(rating, ["AAA", "BBB", "C"])

    def test_edge_case_credit_score(self):
        """Test edge case for low credit score."""
        data = [{
            "credit_score": 649,
            "loan_amount": 100000,
            "property_value": 120000,
            "annual_income": 40000,
            "debt_amount": 25000,
            "loan_type": "adjustable",
            "property_type": "condo"
        }]
        payload = json.dumps(data)
        rating = calculate_credit_rating(payload)
        self.assertEqual(rating, "C")

    def test_invalid_missing_attribute(self):
        """Test mortgage with missing required field."""
        data = [{
            "credit_score": 700,
            "loan_amount": 100000,
            "property_value": 120000,
            "annual_income": 40000,
            "debt_amount": 25000,
            "loan_type": "fixed"
        }]  # missing 'property_type'
        payload = json.dumps(data)
        with self.assertRaises(ValueError):
            calculate_credit_rating(payload)

    def test_zero_property_value(self):
        """Test LTV calculation with zero property value."""
        data = [{
            "credit_score": 700,
            "loan_amount": 100000,
            "property_value": 0,  # Invalid
            "annual_income": 50000,
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "house"
        }]
        payload = json.dumps(data)
        with self.assertRaises(ValueError):
            calculate_credit_rating(payload)

    def test_zero_annual_income(self):
        """Test DTI calculation with zero income."""
        data = [{
            "credit_score": 700,
            "loan_amount": 100000,
            "property_value": 120000,
            "annual_income": 0,  # Invalid
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "house"
        }]
        payload = json.dumps(data)
        with self.assertRaises(ValueError):
            calculate_credit_rating(payload)

    def test_empty_mortgages(self):
        """Test empty mortgages list."""
        data = []
        with self.assertRaises(ValueError):
            calculate_credit_rating(data)

if __name__ == "__main__":
    unittest.main()
