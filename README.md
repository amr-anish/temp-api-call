# temp-api-call

## Video



https://github.com/user-attachments/assets/95d96dcf-a05d-4e1e-acbd-b12fbf66f9a3



## Overview

This project demonstrates a simple REST API to simulate and fetch temperature sensor data. It uses a lightweight SQLite database for quick setup, closely resembling MySQL in structure and usage, making it ideal for proof-of-concept development.

### Key Features

- **FastAPI** & **Uvicorn**: High-performance API framework and server.
- **SQLAlchemy**: ORM for database interaction.
- **Pydantic**: Data validation and settings management.
- **SQLite**: Lightweight, file-based database.
- **pytest**: Testing framework for writing unit tests.

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/temp-api-call.git
cd temp-api-call
```

### 2. Create and activate a virtual environment

#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the API Server

Start the development server using Uvicorn:

Since I have integrated the uvicorn server in main function
running the main.py should do the job
```bash
cd api
python main.py 
```

or

```bash
cd api
uvicorn main:app --reload
```


## Running Tests

```bash
pytest test.py
```

## Calling the APIs using Postman

> ⚠️ Make sure **Postman** is installed before proceeding.

1. Import the `Sensor Rest APIs.postman_collection.json` file into Postman.
2. Modify the JSON body in any request and hit **Send**!

---

## Types of Endpoints

### 1. `POST /sensorapi/data`

Adds/inserts new sensor data.

**Request Body:**
```json
{
  "sensor_id": "2",
  "metric": "Humidity",
  "value": 53.9,
  "timestamp": "2025-04-02T11:00:00"
}
```

- `sensor_id` – required  
- `metric` – required  
- `value` – required  
- `timestamp` – optional (defaults to current time)

> Preloaded metrics in the database:
> - Temperature
> - Humidity
> - Air Quality

---

### 2. `GET /sensorapi/data`

Fetch all the sensor data from the db

---

### 3. `POST /sensorapi/query`

Queries data based on filters like time range, sensor ID, metrics, and aggregation function.

**Request Body Example:**
```json
{
  "sensor_id": ["1"],
  "start_date": "2025-04-01T00:00:00",
  "end_date": "2025-04-04T23:59:59",
  "metrics": ["Temperature", "Air Quality"],
  "stats": "max"
}
```

**Body Parameters:**
- `sensor_id`: list of sensor IDs (**required**)
- `start_date`: ISO format datetime (**optional**)
- `end_date`: ISO format datetime (**optional**)
- `metrics`: list of metrics to filter (**at least one required**)
- `stats`: aggregation function (**min**, **max**, **sum**, or **average**)

---
