from src.database import get_connection

HIGH_SEVERITY_RULES = {
    "TAX_ID_REQUIRED",
    "REGISTRATION_NUMBER_REQUIRED",
    "DOCUMENT_EXPIRY"
}

LOW_SEVERITY_RULES = {
    "EMAIL_FORMAT",
    "PHONE_FORMAT"
}

def determine_severity(validation_rule):

    if validation_rule in HIGH_SEVERITY_RULES:
        return "HIGH"

    if validation_rule in LOW_SEVERITY_RULES:
        return "LOW"

    return "MEDIUM"


def create_exceptions():
    
    connection = get_connection()
    cursor = connection.cursor()

    # Make the operation safely rerunnable.
    cursor.execute(
        "TRUNCATE TABLE exceptions RESTART IDENTITY;"
    )

    # Retrieve all failed validations.
    cursor.execute("""
        SELECT
            client_id,
            validation_rule,
            validation_message
        FROM validation_results
        WHERE validation_status = 'FAIL'
        ORDER BY client_id;
    """)

    failures = cursor.fetchall()

    for client_id, rule, message in failures:

        severity = determine_severity(rule)

        cursor.execute(
            """
            INSERT INTO exceptions (
                client_id,
                exception_type,
                severity,
                description,
                resolution_status
            )
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                client_id,
                rule,
                severity,
                message,
                "OPEN"
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Created {len(failures)} exception records."
    )


if __name__ == "__main__":
    create_exceptions()