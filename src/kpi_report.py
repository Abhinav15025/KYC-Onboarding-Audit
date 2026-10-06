import pandas as pd
from src.database import get_connection, get_engine

def get_kpi_data():

    engine = get_engine()

    decision_query = """
        SELECT
            decision,
            COUNT(*) AS total
        FROM onboarding_decisions
        GROUP BY decision
        ORDER BY decision;
    """

    decisions = pd.read_sql(
        decision_query,
        engine
    )

    exception_query = """
        SELECT
            COUNT(*) AS total_exceptions,

            COUNT(*) FILTER (
                WHERE resolution_status = 'OPEN'
            ) AS open_exceptions,

            COUNT(*) FILTER (
                WHERE resolution_status = 'RESOLVED'
            ) AS resolved_exceptions,

            COUNT(*) FILTER (
                WHERE severity = 'HIGH'
                  AND resolution_status = 'OPEN'
            ) AS open_high_severity

        FROM exceptions;
    """

    exception_summary = pd.read_sql(
        exception_query,
        engine
    )

    affected_clients_query = """
        SELECT
            COUNT(DISTINCT client_id) AS clients_with_exceptions
        FROM exceptions;
    """

    affected_clients = pd.read_sql(
        affected_clients_query,
        engine
    )

    processing_query = """
        SELECT
            AVG(processing_time_seconds)
            AS average_processing_seconds
        FROM audit_logs;
    """

    processing = pd.read_sql(
        processing_query,
        engine
    )

    exception_type_query = """
        SELECT
            exception_type,
            COUNT(*) AS total_exceptions
        FROM exceptions
        GROUP BY exception_type
        ORDER BY total_exceptions DESC;
    """

    exception_types = pd.read_sql(
        exception_type_query,
        engine
    )

    engine.dispose()

    total_clients = decisions["total"].sum()

    pass_count = int(
        decisions.loc[
            decisions["decision"] == "PASS",
            "total"
        ].sum()
    )

    review_count = int(
        decisions.loc[
            decisions["decision"] == "REVIEW",
            "total"
        ].sum()
    )

    remediate_count = int(
        decisions.loc[
            decisions["decision"] == "REMEDIATE",
            "total"
        ].sum()
    )

    clients_with_exceptions = int(
        affected_clients.loc[
            0,
            "clients_with_exceptions"
        ]
    )

    straight_through_rate = (
        pass_count / total_clients * 100
        if total_clients > 0
        else 0
    )

    exception_rate = (
        clients_with_exceptions / total_clients * 100
        if total_clients > 0
        else 0
    )

    average_processing_seconds = float(
        processing.loc[
            0,
            "average_processing_seconds"
        ]
    )

    return {
        "total_clients": int(total_clients),
        "pass_count": pass_count,
        "review_count": review_count,
        "remediate_count": remediate_count,
        "straight_through_rate": straight_through_rate,
        "clients_with_exceptions": clients_with_exceptions,
        "exception_rate": exception_rate,
        "total_exceptions": int(
            exception_summary.loc[
                0,
                "total_exceptions"
            ]
        ),
        "open_exceptions": int(
            exception_summary.loc[
                0,
                "open_exceptions"
            ]
        ),
        "resolved_exceptions": int(
            exception_summary.loc[
                0,
                "resolved_exceptions"
            ]
        ),
        "open_high_severity": int(
            exception_summary.loc[
                0,
                "open_high_severity"
            ]
        ),
        "average_processing_seconds":
            average_processing_seconds,
        "exception_types": exception_types
    }


def print_report(kpis):

    print("\n")
    print("=" * 55)
    print("       KYC CLIENT ONBOARDING OPERATIONS REPORT")
    print("=" * 55)

    print("\nCLIENT PROCESSING")
    print("-" * 55)

    print(
        f"Total Clients Processed:     "
        f"{kpis['total_clients']}"
    )

    print(
        f"Automatically Passed:        "
        f"{kpis['pass_count']}"
    )

    print(
        f"Sent for Review:             "
        f"{kpis['review_count']}"
    )

    print(
        f"Requires Remediation:        "
        f"{kpis['remediate_count']}"
    )

    print(
        f"Straight-Through Rate:       "
        f"{kpis['straight_through_rate']:.2f}%"
    )

    print("\nEXCEPTION MANAGEMENT")
    print("-" * 55)

    print(
        f"Clients with Exceptions:     "
        f"{kpis['clients_with_exceptions']}"
    )

    print(
        f"Exception Rate:              "
        f"{kpis['exception_rate']:.2f}%"
    )

    print(
        f"Total Exceptions:            "
        f"{kpis['total_exceptions']}"
    )

    print(
        f"Open Exceptions:             "
        f"{kpis['open_exceptions']}"
    )

    print(
        f"Resolved Exceptions:         "
        f"{kpis['resolved_exceptions']}"
    )

    print(
        f"Open High-Severity:          "
        f"{kpis['open_high_severity']}"
    )

    print("\nPROCESSING PERFORMANCE")
    print("-" * 55)

    print(
        f"Average Stage Processing:    "
        f"{kpis['average_processing_seconds']:.2f} seconds"
    )

    print("\nTOP EXCEPTION TYPES")
    print("-" * 55)

    print(
        kpis["exception_types"].to_string(
            index=False
        )
    )

    print("\n" + "=" * 55)


if __name__ == "__main__":

    kpis = get_kpi_data()

    print_report(kpis)