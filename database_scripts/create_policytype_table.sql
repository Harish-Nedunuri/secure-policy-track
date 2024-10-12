CREATE TABLE insurance.policy_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,   -- e.g., "auto", "home", "life", "health"
    description TEXT
);
