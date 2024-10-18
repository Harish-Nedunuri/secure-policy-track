# Database SQL queries documentation

## Mock data is generated using [Mockaroo](https://www.mockaroo.com/)

## Database schema is generated using [dbdiagram.io](https://dbdiagram.io/home) using below schema

``` DBML

Project InsuranceDatabase {
  database_type: "PostgreSQL"
}

Table policies {
  id SERIAL [pk, increment] // Primary Key
  policy_number VARCHAR(50) [unique, not null]
  policyholder_id INT [ref: > policyholders.id]
  policy_type_id INT [ref: > policy_types.id]
  premium_amount NUMERIC(10, 2) [not null]
  coverage_amount NUMERIC(10, 2)
  status VARCHAR(20) [not null]  // active, cancelled, expired, etc.
  start_date DATE [not null]
  end_date DATE
  created_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]

  Indexes {
    policy_number [unique]
  }
}

Table policy_types {
  id SERIAL [pk, increment] // Primary Key
  type_name VARCHAR(50) [unique, not null] // e.g., "auto", "home", "life", "health"
  description TEXT
}

Table policyholders {
  id SERIAL [pk, increment] // Primary Key
  full_name VARCHAR(100) [not null]
  address TEXT
  email VARCHAR(100) [unique]
  phone_number VARCHAR(100)
  created_at TIMESTAMP [default: `CURRENT_TIMESTAMP`]

  Indexes {
    email [unique]
  }
} 

```
