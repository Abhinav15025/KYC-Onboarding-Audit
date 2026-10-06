from datetime import datetime, timedelta
import random

from src.database import get_connection
random.seed(200)

WORKFLOW_STAGES = [
    "CLIENT_RECEIVED",
    "VALIDATION_STARTED",
    "VALIDATION_COMPLETED",
    "DECISION_GENERATED",
    "EXCEPTION_CREATED"
]

def generate_workflow_timestamps(client_id):

    start_time = datetime.now() - timedelta(
        minutes=random.randint(30, 600)
    )

    timestamps = {}

    current_time = start_time

    for stage in WORKFLOW_STAGES:

        timestamps[stage] = current_time

        if stage == "CLIENT_RECEIVED":

            duration = random.randint(5, 30)

        elif stage == "VALIDATION_STARTED":

            duration = random.randint(2, 10)

        elif stage == "VALIDATION_COMPLETED":

            duration = random.randint(1, 5)

        elif stage == "DECISION_GENERATED":

            duration = random.randint(1, 5)

        else:

            duration = random.randint(1, 3)

        current_time += timedelta(
            minutes=duration
        )

    return timestamps


def create_audit_logs():

    connection = get_connection()
    cursor = connection.cursor()

    # Clear existing simulated audit logs
    cursor.execute(
        "TRUNCATE TABLE audit_logs RESTART IDENTITY;"
    )

    cursor.execute("""
        SELECT client_id
        FROM clients
        ORDER BY client_id;
    """)

    clients = cursor.fetchall()

    total_logs = 0

    for (client_id,) in clients:

        timestamps = generate_workflow_timestamps(
            client_id
        )

        for stage in WORKFLOW_STAGES:

            started_at = timestamps[stage]

            # Each stage gets a short simulated duration.
            completed_at = (
                started_at
                + timedelta(
                    seconds=random.randint(10, 120)
                )
            )

            processing_time = (
                completed_at - started_at
            ).total_seconds()

            cursor.execute(
                """
                INSERT INTO audit_logs (
                    client_id,
                    workflow_stage,
                    status,
                    started_at,
                    completed_at,
                    processing_time_seconds,
                    notes
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                );
                """,
                (
                    client_id,
                    stage,
                    "COMPLETED",
                    started_at,
                    completed_at,
                    processing_time,
                    "Simulated workflow event."
                )
            )

            total_logs += 1

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Created {total_logs} audit log records."
    )


if __name__ == "__main__":
    create_audit_logs()