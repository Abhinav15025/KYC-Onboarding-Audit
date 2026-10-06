import pandas as pd
from src.database import get_connection

def load_documents(file_path="data/documents.csv"):

    df = pd.read_csv(file_path)

    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO documents (
            client_id,
            document_type,
            document_number,
            issue_date,
            expiry_date,
            document_status
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    for _, row in df.iterrows():

        document_number = (
            None
            if pd.isna(row["document_number"])
            else row["document_number"]
        )

        cursor.execute(
            insert_query,
            (
                int(row["client_id"]),
                row["document_type"],
                document_number,
                row["issue_date"],
                row["expiry_date"],
                row["document_status"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Successfully loaded "
        f"{len(df)} document records into PostgreSQL."
    )


if __name__ == "__main__":
    load_documents()