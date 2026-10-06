from datetime import date, timedelta
import random

import pandas as pd
from faker import Faker

from src.database import get_connection


fake = Faker()
random.seed(100)
Faker.seed(100)


DOCUMENT_TYPES = [
    "BUSINESS_REGISTRATION",
    "TAX_CERTIFICATE",
    "DIRECTOR_ID"
]


def get_client_ids():
    """
    Retrieve all client IDs currently stored in PostgreSQL.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT client_id
        FROM clients
        ORDER BY client_id;
    """)

    client_ids = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return client_ids


def generate_documents(client_ids):
    """
    Generate three KYC documents for each client.

    Normal documents always receive an expiry date
    in the future. Expired documents are introduced
    separately by introduce_document_issues().
    """

    documents = []

    today = date.today()

    for client_id in client_ids:

        for document_type in DOCUMENT_TYPES:

            issue_date = fake.date_between(
                start_date="-3y",
                end_date="-30d"
            )

            expiry_date = today + timedelta(
                days=random.randint(180, 1825)
            )

            document = {
                "client_id": client_id,
                "document_type": document_type,
                "document_number": (
                    f"{document_type[:3]}-"
                    f"{random.randint(100000, 999999)}"
                ),
                "issue_date": issue_date,
                "expiry_date": expiry_date,
                "document_status": "VALID"
            }

            documents.append(document)

    return pd.DataFrame(documents)


def introduce_document_issues(df):
    """
    Introduce controlled document-quality issues.
    """

    # 1. Exactly 10 expired documents
    expired_records = df.sample(
        10,
        random_state=101
    ).index

    df.loc[
        expired_records,
        "expiry_date"
    ] = date.today() - timedelta(days=30)

    df.loc[
        expired_records,
        "document_status"
    ] = "EXPIRED"


    # 2. Exactly 6 missing document numbers
    missing_numbers = df.sample(
        6,
        random_state=102
    ).index

    df.loc[
        missing_numbers,
        "document_number"
    ] = None


    # 3. Exactly 5 invalid document numbers
    invalid_numbers = df.sample(
        5,
        random_state=103
    ).index

    df.loc[
        invalid_numbers,
        "document_number"
    ] = "INVALID-DOC"


    return df


def save_documents(
    df,
    file_path="data/documents.csv"
):
    """
    Save generated document records to CSV.
    """

    df.to_csv(
        file_path,
        index=False
    )


if __name__ == "__main__":

    client_ids = get_client_ids()

    print(
        f"Found {len(client_ids)} clients in PostgreSQL."
    )

    documents_df = generate_documents(
        client_ids
    )

    documents_df = introduce_document_issues(
        documents_df
    )

    save_documents(
        documents_df
    )

    print(
        f"Generated {len(documents_df)} document records."
    )

    print(
        "Saved to data/documents.csv"
    )