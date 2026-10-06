import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection

def get_engine():

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )

    return create_engine(database_url)

def get_clients():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            client_id,
            company_name,
            registration_number,
            tax_id,
            incorporation_date,
            address,
            email,
            phone
        FROM clients
        ORDER BY client_id;
    """)

    clients = cursor.fetchall()

    cursor.close()
    connection.close()

    return clients


def get_documents():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            document_id,
            client_id,
            document_type,
            document_number,
            issue_date,
            expiry_date,
            document_status
        FROM documents
        ORDER BY document_id;
    """)

    documents = cursor.fetchall()

    cursor.close()
    connection.close()

    return documents


