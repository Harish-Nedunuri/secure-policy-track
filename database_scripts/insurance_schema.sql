CREATE TABLE "policies" (
  "id" SERIAL PRIMARY KEY,
  "policy_number" VARCHAR(50) UNIQUE NOT NULL,
  "policyholder_id" INT,
  "policy_type_id" INT,
  "premium_amount" NUMERIC(10,2) NOT NULL,
  "coverage_amount" NUMERIC(10,2),
  "status" VARCHAR(20) NOT NULL,
  "start_date" DATE NOT NULL,
  "end_date" DATE,
  "created_at" TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "policy_types" (
  "id" SERIAL PRIMARY KEY,
  "type_name" VARCHAR(50) UNIQUE NOT NULL,
  "description" TEXT
);

CREATE TABLE "policyholders" (
  "id" SERIAL PRIMARY KEY,
  "full_name" VARCHAR(100) NOT NULL,
  "address" TEXT,
  "email" VARCHAR(100) UNIQUE,
  "phone_number" VARCHAR(100),
  "created_at" TIMESTAMP DEFAULT (CURRENT_TIMESTAMP)
);

CREATE UNIQUE INDEX ON "policies" ("policy_number");

CREATE UNIQUE INDEX ON "policyholders" ("email");

ALTER TABLE "policies" ADD FOREIGN KEY ("policyholder_id") REFERENCES "policyholders" ("id");

ALTER TABLE "policies" ADD FOREIGN KEY ("policy_type_id") REFERENCES "policy_types" ("id");
