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
git clone https://github.com/balagrivine/savannah-informatics-technical-challenge
````

2. Go To The Project Root Directory

````bash
cd savannah-informatics-technical-challenge
````

3. Create a Python3.12 virtual environment and activate it

````bash
python3.12 -m venv env
source env/bin/activate
````

4. Install dependencies
````bash
pip install -r requirements.txt
````

5. Migrate the database schema to apply them locally
````bash
psql -U <user> - h <host> -a scripts/create_tables.sql
````

6. Running tests and generating coverage reports

You need to configure environment variables for this to work as expected
Copy the content on .env.example to .env file:

````bash
cp .env.example .env
````

The env file should look like this abd you can change the values  to your own preference

````bash
# Database Configurations
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_USER = "user"
DB_NAME = "customer_order_service"
DB_PASSWORD = "password"

# Google credentials to configure OAuth2.0
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""

# Africa's Talking Bulk SMS Configurations
BASE_LIVE_ENDPOINT    = " "
BASE_SANDBOX_ENDPOINT = " "
API_KEY               = " "
USERNAME              = " "
````

````bash
pytest --cov --cov-report=xml
````

7. Run the application
````bash
python3 -m uvicorn main:app
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
