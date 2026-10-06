-- ==========================================
-- CLIENTS
-- ==========================================

CREATE TABLE IF NOT EXISTS clients (
    client_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    registration_number VARCHAR(50),
    tax_id VARCHAR(50),
    incorporation_date DATE,
    address TEXT,
    email VARCHAR(150),
    phone VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ==========================================
-- DOCUMENTS
-- ==========================================

CREATE TABLE IF NOT EXISTS documents (
    document_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    document_number VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    document_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_documents_client
        FOREIGN KEY (client_id)
        REFERENCES clients(client_id)
        ON DELETE CASCADE
);


-- ==========================================
-- VALIDATION RESULTS
-- ==========================================

CREATE TABLE IF NOT EXISTS validation_results (
    validation_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    validation_rule VARCHAR(100) NOT NULL,
    validation_status VARCHAR(20) NOT NULL,
    validation_message TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_validation_client
        FOREIGN KEY (client_id)
        REFERENCES clients(client_id)
        ON DELETE CASCADE
);


-- ==========================================
-- EXCEPTIONS
-- ==========================================

CREATE TABLE IF NOT EXISTS exceptions (
    exception_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    exception_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    resolution_status VARCHAR(30) DEFAULT 'OPEN',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,

    CONSTRAINT fk_exception_client
        FOREIGN KEY (client_id)
        REFERENCES clients(client_id)
        ON DELETE CASCADE
);


-- ==========================================
-- AUDIT LOGS
-- ==========================================

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    workflow_stage VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    processing_time_seconds NUMERIC(10,2),
    notes TEXT,

    CONSTRAINT fk_audit_client
        FOREIGN KEY (client_id)
        REFERENCES clients(client_id)
        ON DELETE CASCADE
);