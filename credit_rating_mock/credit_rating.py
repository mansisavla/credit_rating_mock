from enum import Enum
from typing import List, Dict
import json

class LoanType(Enum):
    FIXED = "fixed"
    ADJUSTABLE = "adjustable"

class PropertyType(Enum):
    CONDO = "condo"
    HOUSE = "house"

def ltv_eval(loan_amount: float, property_value: float) -> float:
    """
    Calculate Loan-to-Value ratio.
    Args:
        loan_amount (float): The total loan amount of the mortgage.
        property_value (float): The type of property, e.g., "condo", "house", etc.
    Returns:
        float: The Loan-to-Value ratio as a percentage.
    """
    if property_value == 0:
        raise ValueError("Property value cannot be zero.")
    
    return (loan_amount / property_value) * 100

def dti_eval(debt_amount: float, annual_income: float) -> float:
    """
    Calculate Debt-to-Income ratio.
    Args:
        debt_amount (float):  The borrower’s existing debt amount.
        annual_income (float): The borrower’s annual income.
    Returns:
        float: The Debt-to-Income ratio as a percentage.
    """
    if annual_income == 0:
        raise ValueError("Annual income cannot be zero.")
    
    return (debt_amount / annual_income) * 100

def risk_eval(mortgage: List[Dict]) -> str:
    """
    Calculates the risk score for a mortgage based on various financial and property factors.
    
    Args:
        mortgage (List[Dict]): A dictionary containing the following keys:
            - "loan_amount" (float): The total loan amount of the mortgage.
            - "property_value" (float): The value of the mortgaged property.
            - "debt_amount" (float):  The borrower’s existing debt amount.
            - "annual_income" (float): The borrower’s annual income.
            - "credit_score" (int): The credit score of the borrower.
            - "loan_type" (str): The type of loan, either "fixed" or "adjustable".
            - "property_type" (str): The type of property, e.g., "condo", "house", etc.
    Returns:
        str: The calculated risk score as a string.
    """
    try:
        risk_score = 0

        ltv = ltv_eval(float(mortgage["loan_amount"]), float(mortgage["property_value"]))
        dti = dti_eval(float(mortgage["debt_amount"]), float(mortgage["annual_income"]))

        if ltv > 90.0:
            risk_score += 2
        elif ltv > 80.0:
            risk_score += 1

        if dti > 50.0:
            risk_score += 2
        elif dti > 40.0:
            risk_score += 1

        credit_score = mortgage["credit_score"]
        if credit_score >= 700:
            risk_score -= 1
        elif credit_score < 650:
            risk_score += 1

        if LoanType(mortgage["loan_type"]) == LoanType.FIXED:
            risk_score -= 1
        elif LoanType(mortgage["loan_type"]) == LoanType.ADJUSTABLE:
            risk_score += 1

        if PropertyType(mortgage["property_type"]) == PropertyType.CONDO:
            risk_score += 1

        return str(risk_score)
    except KeyError as e:
        raise ValueError(f"Missing required mortgage field: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid value in mortgage data: {e}")
    except TypeError as e:
        raise ValueError(f"Invalid data type in mortgage: {e}")

def calculate_credit_rating(mortgages_payload: str) -> str:
    """
    Credit rating calculation logic for residential mortgage-backed 
    securities (RMBS).

    Args:
        mortgages_payload (str): A JSON string containing a list of mortgages,
    Returns:
        str: The calculated credit rating as a string ("AAA", "BBB", or "C").

    Raises:
        ValueError: If the mortgages list is empty or contains invalid data.
    """
    if not mortgages_payload:
        raise ValueError("The mortgages_payload cannot be empty.")

    try:
        data = json.loads(mortgages_payload)
        if not isinstance(data, list):
            raise ValueError("Invalid data format. Expected a list of mortgages.")
        if not data:
            raise ValueError("The mortgages list cannot be empty.")
        
        risk_score = [int(risk_eval(mortgage)) for mortgage in data]

        avg_score = sum(mortgage["credit_score"] for mortgage in data) / len(data)
        total_risk_calculated = sum(risk_score)

        if avg_score >= 700:
            total_risk_calculated -= 1
        elif avg_score < 650:
            total_risk_calculated += 1

        if total_risk_calculated <= 2:
            return "AAA"
        elif 3 <= total_risk_calculated <= 5:
            return "BBB"
        else:
            return "C"
    except KeyError as e:
        raise ValueError(f"Missing required mortgage field: {e}")
    except TypeError as e:
        raise ValueError(f"Invalid data type in mortgages: {e}")