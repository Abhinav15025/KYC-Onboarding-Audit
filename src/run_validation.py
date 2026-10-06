from src.database import (
    get_connection,
    get_clients,
    get_documents
)

from src.validation_engine import (
    validate_required,
    validate_tax_id,
    validate_registration_number,
    validate_email,
    validate_phone,
    validate_document_number,
    validate_expiry_date
)


def save_validation_result(
    client_id,
    rule,
    status,
    message
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO validation_results (
            client_id,
            validation_rule,
            validation_status,
            validation_message
        )
        VALUES (%s, %s, %s, %s);
        """,
        (
            client_id,
            rule,
            status,
            message
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def validate_client(client):

    (
        client_id,
        company_name,
        registration_number,
        tax_id,
        incorporation_date,
        address,
        email,
        phone
    ) = client

    results = []

    # Company name
    if validate_required(company_name):
        results.append(
            (
                client_id,
                "COMPANY_NAME_REQUIRED",
                "PASS",
                "Company name is present."
            )
        )
    else:
        results.append(
            (
                client_id,
                "COMPANY_NAME_REQUIRED",
                "FAIL",
                "Company name is missing."
            )
        )

    # Registration number
    if not validate_required(registration_number):

        results.append(
            (
                client_id,
                "REGISTRATION_NUMBER_REQUIRED",
                "FAIL",
                "Registration number is missing."
            )
        )

    elif validate_registration_number(
        registration_number
    ):

        results.append(
            (
                client_id,
                "REGISTRATION_NUMBER_FORMAT",
                "PASS",
                "Registration number format is valid."
            )
        )

    else:

        results.append(
            (
                client_id,
                "REGISTRATION_NUMBER_FORMAT",
                "FAIL",
                "Registration number format is invalid."
            )
        )

    # Tax ID
    if not validate_required(tax_id):

        results.append(
            (
                client_id,
                "TAX_ID_REQUIRED",
                "FAIL",
                "Tax ID is missing."
            )
        )

    elif validate_tax_id(tax_id):

        results.append(
            (
                client_id,
                "TAX_ID_FORMAT",
                "PASS",
                "Tax ID format is valid."
            )
        )

    else:

        results.append(
            (
                client_id,
                "TAX_ID_FORMAT",
                "FAIL",
                "Tax ID format is invalid."
            )
        )

    # Email
    if validate_email(email):

        results.append(
            (
                client_id,
                "EMAIL_FORMAT",
                "PASS",
                "Email format is valid."
            )
        )

    else:

        results.append(
            (
                client_id,
                "EMAIL_FORMAT",
                "FAIL",
                "Email format is invalid."
            )
        )

    # Phone
    if validate_phone(phone):

        results.append(
            (
                client_id,
                "PHONE_FORMAT",
                "PASS",
                "Phone number format is valid."
            )
        )

    else:

        results.append(
            (
                client_id,
                "PHONE_FORMAT",
                "FAIL",
                "Phone number format is invalid."
            )
        )

    return results


def validate_document(document):
    """
    Run all document-level validation rules.
    """

    (
        document_id,
        client_id,
        document_type,
        document_number,
        issue_date,
        expiry_date,
        document_status
    ) = document

    results = []

    # Document number
    if validate_document_number(
        document_number
    ):

        results.append(
            (
                client_id,
                "DOCUMENT_NUMBER_FORMAT",
                "PASS",
                f"{document_type} number format is valid."
            )
        )

    else:

        results.append(
            (
                client_id,
                "DOCUMENT_NUMBER_FORMAT",
                "FAIL",
                f"{document_type} number is missing or invalid."
            )
        )

    # Expiry
    if validate_expiry_date(expiry_date):

        results.append(
            (
                client_id,
                "DOCUMENT_EXPIRY",
                "PASS",
                f"{document_type} is not expired."
            )
        )

    else:

        results.append(
            (
                client_id,
                "DOCUMENT_EXPIRY",
                "FAIL",
                f"{document_type} has expired."
            )
        )

    return results


def run_validation():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "TRUNCATE TABLE validation_results RESTART IDENTITY;"
    )

    connection.commit()

    cursor.close()
    connection.close()

    clients = get_clients()
    documents = get_documents()

    print(
        f"Validating {len(clients)} clients "
        f"and {len(documents)} documents..."
    )

    total_results = 0

    for client in clients:

        results = validate_client(client)

        for result in results:

            save_validation_result(*result)

            total_results += 1

    for document in documents:

        results = validate_document(document)

        for result in results:

            save_validation_result(*result)

            total_results += 1

    print(
        f"Validation completed. "
        f"Generated {total_results} validation results."
    )


if __name__ == "__main__":
    run_validation()