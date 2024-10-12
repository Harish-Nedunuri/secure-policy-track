CREATE TABLE insurance.policies (
    id SERIAL PRIMARY KEY,
    policy_number VARCHAR(50) NOT NULL UNIQUE,
    policyholder_id INT REFERENCES insurance.policyholders(id),
    policy_type_id INT REFERENCES insurance.policy_types(id),
    premium_amount NUMERIC(10, 2) NOT NULL,
    coverage_amount NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL,   -- active, cancelled, expired, etc.
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
