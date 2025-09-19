# Savannah Informatics Technical Challenge

[![codecov](https://codecov.io/gh/balagrivine/savannah-informatics-technical-challenge/graph/badge.svg?token=46HVRUE4WI)](https://codecov.io/gh/balagrivine/savannah-informatics-technical-challenge)

This is a web service project developed using the Python FastAPI Framework with Postgres database.

## Features
* Create and manage customers.
  * Authentication and authorization
* Create and manage orders
* When an order is added, send the customer an SMS alerting them

The project is equipped with tests and code coverage metrics using codecov which are all integrated into the CI/CD pipeline. The deployed version of the project is accessible on Azure.

## Getting started
1. Clone the repo

````bash
git clone https://github.com/Lucky123-cloud/savannah-informatics-technical-challenge.git
````

2. Go To The Project Root Directory

````bash
cd savannah-informatics-technical-challenge
````

3. Create a Python3.12 virtual environment and activate it

````bash
python -m venv env
.\env\Scripts\Activate
````

4. Install dependencies
````bash
pip install -r requirements.txt
````

5. Migrate the database schema to apply them locally
````bash
psql -U <user> - h <host> -a scripts/create_tables.sql
psql -U postgres -h localhost -d savannah_db -a -f scripts/create_tables.sql

````


6. Running tests and generating coverage reports

You need to configure environment variables for this to work as expected
Copy the content on .env.example to .env file:

````bash
cp .env.example .env
````

The env file should look like this and make sue to change the values to your own prefences

````bash
# Database Configurations
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_USER = "postgres"
DB_NAME = "savannah_db"
DB_PASSWORD = "your_own_password_you_set_up_during_postgres_installation"

# Google credentials to configure OAuth2.0
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""

# Africa's Talking Bulk SMS Configurations
BASE_LIVE_ENDPOINT    = " "
BASE_SANDBOX_ENDPOINT = " "
API_KEY               = " "
USERNAME              = " "
````

# Add your secret key - is used to sign the session cookies, so nobody can tamper with them.
You can generate them this way:

import secrets
print(secrets.token_hex(32))

or:

Just use a secret_key of your liking like "supersecretkey"

SECRET_KEY= " "

````

###Algorithm
The algorithm defines how JSON Web Tokens (JWTs) are signed and verified.  
This project uses **HS256 (HMAC with SHA-256)**, which relies on a shared secret key for both signing and verification.  
It ensures tokens are secure and tamper-proof, enabling safe authentication and authorization.
So add it in your .env file like this -> ALGORITHM=""


````bash
pytest --cov --cov-report=xml
````

7. Run the application
````bash
python -m uvicorn src.main:app
````

### Running the application in a Docker container

Build a docker image with the command below
````bash
docker buildx build -t ecommerce:latest .
````

Run the image after a successful build

````bash
docker run -p 8080:8080 ecommerce
````
You can now access your application over here [locahost](http://127.0.0.1:8080)

## CI/CD Workflow
My CI/CD workflow is powered by GitHub Actions. Inside the pipeline I have steps to run automated tests and collect coverage reports during the build stage. The workflow automates deployment to an Azure app service accessible on [here](https://savannah-dxcwbscyexfyf5ft.eastus2-01.azurewebsites.net/)
