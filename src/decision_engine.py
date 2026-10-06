from collections import defaultdict
from src.database import get_connection


CRITICAL_RULES = {
    "TAX_ID_REQUIRED",
    "REGISTRATION_NUMBER_REQUIRED",
    "DOCUMENT_EXPIRY"
}


def get_validation_results():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            client_id,
            validation_rule,
            validation_status,
            validation_message
        FROM validation_results
        ORDER BY client_id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    results = defaultdict(list)

    for row in rows:
        client_id = row[0]

        results[client_id].append({
            "rule": row[1],
            "status": row[2],
            "message": row[3]
        })

    return results


def determine_decision(client_results):

    failures = [
        result
        for result in client_results
        if result["status"] == "FAIL"
    ]

    if not failures:

        return {
            "decision": "PASS",
            "risk_score": 0,
            "reason": "All validation rules passed."
        }

    critical_failures = [
        result
        for result in failures
        if result["rule"] in CRITICAL_RULES
    ]

    if critical_failures:

        return {
            "decision": "REMEDIATE",
            "risk_score": 100,
            "reason": (
                "Critical KYC requirement failed: "
                + "; ".join(
                    result["message"]
                    for result in critical_failures
                )
            )
        }

    return {
        "decision": "REVIEW",
        "risk_score": 50,
        "reason": (
            "One or more non-critical "
            "validation rules failed."
        )
    }


def save_decision(
    client_id,
    decision,
    risk_score,
    reason
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO onboarding_decisions (
            client_id,
            decision,
            risk_score,
            reason
        )
        VALUES (%s, %s, %s, %s);
        """,
        (
            client_id,
            decision,
            risk_score,
            reason
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


def run_decision_engine():

    validation_results = get_validation_results()

    print(
        f"Evaluating {len(validation_results)} clients..."
    )

    decision_counts = {
        "PASS": 0,
        "REVIEW": 0,
        "REMEDIATE": 0
    }

    for client_id, results in validation_results.items():

        decision = determine_decision(results)

        save_decision(
            client_id,
            decision["decision"],
            decision["risk_score"],
            decision["reason"]
        )

        decision_counts[
            decision["decision"]
        ] += 1

    print("\nOnboarding Decision Summary")
    print("---------------------------")

    for decision, count in decision_counts.items():

        print(
            f"{decision}: {count}"
        )


if __name__ == "__main__":
    run_decision_engine()