import pandas as pd
from src.database import get_connection

def load_clients(file_path="data/clients.csv"):

    df = pd.read_csv(file_path)

    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO clients (
            client_id,
            company_name,
            registration_number,
            tax_id,
            incorporation_date,
            address,
            email,
            phone
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (client_id) DO NOTHING;
    """

    for _, row in df.iterrows():

        cursor.execute(
            insert_query,
            (
                int(row["client_id"]),
                row["company_name"],
                row["registration_number"],
                row["tax_id"],
                row["incorporation_date"],
                row["address"],
                row["email"],
                row["phone"]
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Successfully loaded {len(df)} client records into PostgreSQL.")


if __name__ == "__main__":
    load_clients()