# Changelog

## 1.0.3 (14/10/2024)

### New Features

- Added terraform main and vairable for resource group and container registry
- Added logging in support utility's
- Added unit test for database support utils and oauth2 using mock credentials

### Fixes

- Included asyncio and asyncpg for concurrent db operations
- GET sucess response for RetreiveTask status is 200 OK not 201 Created
- Password reset
- Restructured the Tests: Unit Tests and DB Integration Tests
- Added env variables in GITHub Secrets

### ToDo

- [x] Set Up the Project Structure & Requirements
- [x] Tests and Functions Oauth using mock credentials
- [x] Logging & Database Setup, Tests, Utilities
- [x] Terraform IaC for resource grp and container registry
- [x] Add mock data to db and setup PgAdmin4 local tool & add SupportUtils
- [x] Create arguments utils and add agrument model RetreiveTask in policy_core package
- [x] create entry and router for RetreiveTask with Oauth2 Dependency injection
- [x] create a Dockerfile, CI-CD pipeline with triggers, Unit Test, Build and Deploy the container to a remote registry.
- [x] Add documentation and doc strings to all functions
- [x] Perform testing and add documentation
