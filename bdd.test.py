"""
CREATE TABLE operations_log (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    data_processed TEXT NOT NULL,
    additional_info TEXT
);


CREATE TABLE errors_log (
    id SERIAL PRIMARY KEY,
    operation_id INTEGER NOT NULL,
    error_time TIMESTAMP NOT NULL,
    error_type VARCHAR(255) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    FOREIGN KEY (operation_id) REFERENCES operations_log (id)
);


CREATE TABLE api_usage_log (
    id SERIAL PRIMARY KEY,
    api_name VARCHAR(255) NOT NULL,
    operation_id INTEGER,
    request_time TIMESTAMP NOT NULL,
    response_status INTEGER NOT NULL,
    data_volume INTEGER,
    FOREIGN KEY (operation_id) REFERENCES operations_log (id)
);
"""