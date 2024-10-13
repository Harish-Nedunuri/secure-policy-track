# SecurePolicyTrack

Secure Policy Track is a API for tracking and managing insurance policies securely. It provides endpoints for  retrieving insurance policies. The API is built using FastAPI and uses a PostgreSQL database for data storage. The API is designed to be secure and scalable, and it uses authentication and authorization mechanisms to ensure that only authorized users can access the data. The API features masking of sensitive data, and it uses encryption to protect the data in transit and at rest.

## Requirements

- Python 3.10 or higher
- PostgreSQL database: pgAdmin4 or any other database management system
- FastAPI
- SQLAlchemy
- PyJWT

## Local Installation

To install the Secure Policy Track API, follow these steps:

- Clone the repository to your local machine.
 ```git clone https://github.com/your-username/secure-policy-track.git```
- Create a virtual environment and activate it.
- ```python -m venv .venv```
- ```source venv/bin/activate``` for Linux/WSL or ```.venv\scripts\activate``` for Windows
- Install the secure_policy_track package and required dependencies by running the following command:
 code ```pip install -e .```
- Create a .env file in the root directory of the project and add the following environment variables:

## Project Structure

The project is

## Docker Build

- Install Docker & Docker Compose on your local machine.
- Navigate to the root directory of the project.
- Run the following command to build the Docker image:

```docker system prune --force```

```docker build -t policytrack:test .```

``` docker run -p 8000:8000 policytrack:test ```

- Open LocalHost:8000  in your web browser to access the API.
