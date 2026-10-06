# Automated KYC & Client Onboarding Audit Workflow

A Python and PostgreSQL-based simulation of an automated corporate
Know-Your-Customer (KYC) onboarding control workflow.

The project demonstrates how structured validation, exception management,
workflow logging, and operational KPI analysis can reduce manual processing
friction in client onboarding.

> This is a simulated educational project using synthetic data. It is not
> a production KYC/AML system and does not perform real regulatory screening.

---

## Project Overview

Corporate client onboarding requires operations teams to validate client
information and supporting documentation before an account can proceed.

This project simulates that workflow by automatically:

- Validating client information
- Checking document formats and expiry dates
- Detecting data-quality exceptions
- Assigning operational severity
- Routing clients into PASS, REVIEW, or REMEDIATE outcomes
- Maintaining an exception queue
- Recording workflow audit events
- Calculating operational KPIs

---

## Workflow Architecture

```text
                    CLIENT ONBOARDING
                           |
              +------------+------------+
              |                         |
              v                         v
         CLIENT DATA              KYC DOCUMENTS
              |                         |
              +------------+------------+
                           |
                           v
                  VALIDATION ENGINE
                           |
                           v
                 VALIDATION RESULTS
                           |
                           v
                  DECISION ENGINE
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
           PASS          REVIEW      REMEDIATE
             |             |             |
             +-------------+-------------+
                           |
                           v
                    EXCEPTION QUEUE
                           |
                           v
                       AUDIT LOGS
                           |
                           v
                    KPI REPORTING


Technology Stack
- Python
- PostgreSQL
- Pandas
- Regex
- psycopg2
- SQLAlchemy
- Faker
- pytest
- python-dotenv

Database Design
The PostgreSQL database contains the following core tables:
clients
Stores corporate client information.

documents
Stores KYC document information associated with each client.

validation_results
Stores the result of each automated validation rule.

onboarding_decisions
Stores the overall onboarding decision for each client.

exceptions
Stores operational issues requiring review or remediation.

audit_logs
Stores simulated workflow events and processing times.

Validation Controls
Client-level controls
- Required company name
- Registration number presence
- Registration number format
- Tax ID presence
- Tax ID format
- Email format
- Phone format
Document-level controls
- Document number format
- Document expiry validation
Exception Severity
The workflow assigns an operational priority to each failed validation.
Severity	Examples
HIGH	Missing Tax ID, missing registration number, expired document
MEDIUM	Invalid Tax ID, invalid registration number, invalid document number
LOW	Invalid email, invalid phone


These severity levels are simplified workflow priorities for this
simulation and are not regulatory risk ratings.
Client Decision Logic
Each client receives an overall onboarding outcome.
Decision	Meaning
PASS	All validation controls passed
REVIEW	Non-critical validation issue requires analyst review
REMEDIATE	Critical onboarding requirement requires corrective action


Simulated Dataset
The project uses synthetic data.
Current demonstration dataset:
- 100 corporate clients
- 300 KYC documents
- 1,100 automated validation checks
- 50 validation exceptions
- 500 simulated workflow audit events
The data intentionally includes:
- Missing fields
- Invalid identifiers
- Invalid email addresses
- Invalid phone numbers
- Duplicate registration numbers
- Missing document numbers
- Invalid document numbers
- Expired documents
Current KPI Results
The current demonstration run produced:
KPI	Result
Clients processed	100
Automatically passed	62
Sent for review	28
Requires remediation	10
Straight-through processing rate	62%
Clients with exceptions	38
Exception rate	38%
Total exceptions	50
Open exceptions	49
Resolved exceptions	1
Open high-severity exceptions	10
Average stage processing time	67.67 seconds


Top Exception Types
Exception	Count
Document number format	11
Tax ID format	10
Document expiry	10
Registration number format	9
Email format	5
Phone format	5


Processing times are simulated for demonstration purposes and should not
be interpreted as real banking operational benchmarks.
Project Structure
KYC Onboarding Audit/
|
├── data/
├── src/
│   ├── database.py
│   ├── data_generator.py
│   ├── document_generator.py
│   ├── load_clients.py
│   ├── load_documents.py
│   ├── validation_engine.py
│   ├── run_validation.py
│   ├── decision_engine.py
│   ├── exception_manager.py
│   ├── audit_logger.py
│   └── kpi_report.py
|
├── sql/
│   └── schema.sql
|
├── tests/
│   ├── test_database.py
│   ├── test_validation.py
│   ├── test_decision_engine.py
│   └── test_exception_manager.py
|
├── .env
├── .gitignore
├── requirements.txt
└── README.md

Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "KYC Onboarding Audit"

2. Create a virtual environment
python -m venv venv

Activate it on Windows:
venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Configure PostgreSQL
Create a PostgreSQL database named:
kyc_audit

Create a .env file:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kyc_audit
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

5. Create database tables
Execute:
sql/schema.sql

inside the kyc_audit PostgreSQL database.
Running the Project
Generate synthetic client data
python -m src.data_generator


Load clients
python -m src.load_clients


Generate KYC documents
python -m src.document_generator


Load documents
python -m src.load_documents


Run validation
python -m src.run_validation


Generate onboarding decisions
python -m src.decision_engine


Create the exception queue
python -m src.exception_manager


Generate audit logs
python -m src.audit_logger


Generate the KPI report
python -m src.kpi_report


Testing
Run the complete test suite:
python -m pytest


The current project contains 14 automated tests covering:
- Database connectivity
- Validation rules
- Decision logic
- Exception severity
Expected result:
14 passed

Operational Design Principles
The project demonstrates several operational control concepts:
Straight-through processing
Valid applications are automatically passed without unnecessary manual
intervention.
Exception management
Invalid records are routed into an exception queue rather than silently
discarded.
Prioritization
Exceptions are assigned severity levels so operations teams can focus on
higher-priority issues first.
Auditability
Workflow events are recorded with timestamps and processing durations.
KPI monitoring
Operational metrics are calculated from the workflow database to identify
processing friction and exception trends.