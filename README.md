# Savannah Informatics Technical Challenge

[![codecov](https://codecov.io/gh/Lucky123-cloud/savannah-informatics-technical-challenge/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/Lucky123-cloud/savannah-informatics-technical-challenge)


This project is a **web service** built using **Python FastAPI** with a **PostgreSQL database**. It allows managing customers and orders, with automated SMS notifications for new orders.

---

## Features

* **Customer Management**

  * Create and manage customers
  * Authentication and authorization (JWT)
* **Order Management**

  * Create and manage orders
  * Sends SMS notifications to customers when an order is created
* **Testing & CI/CD**

  * Unit and integration tests with coverage reports
  * Integrated into CI/CD pipeline with GitHub Actions
* **Deployment**

  * Deployed on Azure for live testing

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Lucky123-cloud/savannah-informatics-technical-challenge.git
```

### 2. Navigate to Project Root

```bash
cd savannah-informatics-technical-challenge
```

### 3. Create and Activate Python Virtual Environment

```bash
python -m venv env
.\env\Scripts\Activate   # Windows
# source env/bin/activate  # Linux / macOS
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up the Database

Migrate database schema locally:

```bash
psql -U postgres -h localhost -d savannah_db -a -f scripts/create_tables.sql
```

Check the connection:

```sql
\conninfo
SELECT * FROM products;
SELECT * FROM customers;
```

---

### 6. Configure Environment Variables

Copy the example `.env`:

```bash
cp .env.example .env
```

Edit the `.env` file with your configurations:

```env
# Database Config
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_NAME=savannah_db
DB_PASSWORD=your_postgres_password

# Google OAuth2
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Africa's Talking SMS
BASE_LIVE_ENDPOINT=
BASE_SANDBOX_ENDPOINT=
AFRICAS_TALKING_API_KEY=
AFRICAS_TALKING_USERNAME=

# Secret key for sessions
SECRET_KEY=supersecretkey

# JWT Algorithm
ALGORITHM=HS256
```

> You can generate a secret key for sessions using:

```python
import secrets
print(secrets.token_hex(32))
```

---

### 7. Running Tests and Coverage Reports

```bash
pytest --cov --cov-report=xml
```

Coverage reports are sent to [Codecov](https://codecov.io/gh/Lucky123-cloud/savannah-informatics-technical-challenge).

---

### 8. Run the Application Locally

```bash
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8001
```

---

### 9. Run the Application in Docker

**Dockerfile** is included. Build and run the container:

```bash
docker buildx build -t ecommerce:latest .
docker run -p 8080:8080 ecommerce
```

> Access your application at: [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## CI/CD Workflow

* Automated tests run via **GitHub Actions** during build
* Coverage reports are collected and sent to **Codecov**
* Automatic deployment to **Azure App Service**
* Live application: [Savannah Web Service](https://savannah-dxcwbscyexfyf5ft.eastus2-01.azurewebsites.net/)

---

### Notes

1. **JWT Authentication**

   * Uses `HS256` algorithm
   * Secret key required in `.env`

2. **SMS Notifications**

   * Powered by Africa’s Talking
   * Ensure valid phone numbers (international format supported)

3. **Database**

   * PostgreSQL is required
   * Ensure tables are created before running
