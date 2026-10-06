from datetime import date, timedelta
from faker import Faker
import random
import pandas as pd

fake = Faker()
random.seed(42)
Faker.seed(42)

def generate_clients(number_of_clients=100):
    clients = []
    for client_id in range(1, number_of_clients + 1):

        incorporation_date = fake.date_between(
            start_date="-10y",
            end_date="-1y"
        )

        client = {
            "client_id": client_id,
            "company_name": fake.company(),
            "registration_number": f"REG{random.randint(100000, 999999)}",
            "tax_id": f"TAX{random.randint(100000000, 999999999)}",
            "incorporation_date": incorporation_date,
            "address": fake.address().replace("\n", ", "),
            "email": fake.company_email(),
            "phone": fake.phone_number()
        }

        clients.append(client)

    return pd.DataFrame(clients)


def introduce_data_issues(df):

    # 1. Missing Tax IDs
    missing_tax_ids = df.sample(5, random_state=42).index
    df.loc[missing_tax_ids, "tax_id"] = None

    # 2. Invalid Tax ID formats
    invalid_tax_ids = df.sample(5, random_state=43).index
    df.loc[invalid_tax_ids, "tax_id"] = "INVALID-TAX-123"

    # 3. Invalid Emails
    invalid_emails = df.sample(5, random_state=44).index
    df.loc[invalid_emails, "email"] = "corrupted_email.com"

    # 4. Missing Registration Numbers
    missing_registration = df.sample(4, random_state=45).index
    df.loc[missing_registration, "registration_number"] = None

    # 5. Duplicate Registration Numbers
    duplicate_targets = df.sample(5, random_state=46).index

    for idx in duplicate_targets:
        df.loc[idx, "registration_number"] = df.loc[0, "registration_number"]

    # 6. Missing Company Names
    missing_company_names = df.sample(3, random_state=47).index
    df.loc[missing_company_names, "company_name"] = None

    # 7. Invalid Phone Numbers
    invalid_phones = df.sample(5, random_state=48).index
    df.loc[invalid_phones, "phone"] = "123-FAIL"

    return df

def save_clients(df, file_path="data/clients.csv"):

    df.to_csv(file_path, index=False)


if __name__ == "__main__":

    clients_df = generate_clients(100)

    clients_df = introduce_data_issues(clients_df)

    save_clients(clients_df)

    print(f"Generated {len(clients_df)} synthetic client records.")
    print(f"Saved to data/clients.csv")