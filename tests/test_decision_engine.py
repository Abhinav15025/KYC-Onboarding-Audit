from src.decision_engine import determine_decision


def test_pass_decision():

    results = [
        {
            "rule": "TAX_ID_FORMAT",
            "status": "PASS",
            "message": "Tax ID format is valid."
        },
        {
            "rule": "EMAIL_FORMAT",
            "status": "PASS",
            "message": "Email format is valid."
        }
    ]

    decision = determine_decision(results)

    assert decision["decision"] == "PASS"
    assert decision["risk_score"] == 0


def test_review_decision():

    results = [
        {
            "rule": "EMAIL_FORMAT",
            "status": "FAIL",
            "message": "Email format is invalid."
        }
    ]

    decision = determine_decision(results)

    assert decision["decision"] == "REVIEW"
    assert decision["risk_score"] == 50


def test_remediate_decision():

    results = [
        {
            "rule": "TAX_ID_REQUIRED",
            "status": "FAIL",
            "message": "Tax ID is missing."
        }
    ]

    decision = determine_decision(results)

    assert decision["decision"] == "REMEDIATE"
    assert decision["risk_score"] == 100