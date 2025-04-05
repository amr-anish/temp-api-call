import pytest
import logging
import warnings
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from main import app, get_db
from model import SensorData


# In this file we will be testing the api layer and its functionality
# So we are mocking the db 

client = TestClient(app)


@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    app.dependency_overrides[get_db] = lambda: db
    return db


def test_adding_the_data_into_the_db(mock_db):

    try:
        # for adding the primary key when it is inserted to the db mocking it
        def refresh_side_effect(obj):
            obj.id = 1
        mock_db.refresh.side_effect = refresh_side_effect

        payload = {
            "sensor_id": "1", 
            "metric": "Temperature", 
            "value": 46.5
            }
        response = client.post("/sensorapi/data/", json=payload)
        logging.info("Add Data Response: %s", response.json())
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["value"] == 46.5
        logging.info("test_adding_the_data_into_the_db passed Successfully")

    except Exception as e:
        pytest.fail(f"Error in test_adding_the_data_into_the_db: {e}")
        


def test_fetching_all_the_data(mock_db):

    try:
        mock_data = [
            SensorData(id=1, sensor_id="1", metric="Temperature", value=46.5),
            SensorData(id=2, sensor_id="2", metric="Humidity", value=75.0)
        ]
        mock_db.query.return_value.all.return_value = mock_data

        response = client.get("/sensorapi/data/")
        logging.info("Get All Data Response: %s", response.json())
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["sensor_id"] == "1"
        logging.info("test_fetching_all_the_data passed Successfully")

    except Exception as e:
        pytest.fail(f"Error in test_fetching_all_the_data: {e}")

def test_get_data_based_on_condition(mock_db):
    try:
        mock_query = mock_db.query.return_value
        mock_query.filter.return_value = mock_query
        mock_query.with_entities.return_value.scalar.return_value = 46.5

        payload = {
            "sensor_id": ["1"],
            "metrics": ["Temperature"],
            "stats": "max"
        }
        response = client.post("/sensorapi/query/", json=payload)
        logging.info("Get Stats Response: %s", response.json())
        assert response.status_code == 200
        assert response.json()["Temperature"] == 46.5
        logging.info("test_get_stats passed Successfully")
    except Exception as e:
        pytest.fail(f"Error in test_get_data_based_on_condition: {e}")


def test_add_data_missing_data_metrics(mock_db):

    try:
        payload = {
            "sensor_id": "1",
            "value": 46.5  
        }
        response = client.post("/sensorapi/data/", json=payload)
        logging.info("Add Data Missing Field Response: %s", response.json())
        assert response.status_code == 422
        logging.info("test_add_data_missing_data_metrics passed Successfully")

    except Exception as e:
        pytest.fail(f"Error in test_add_data_missing_data_metrics: {e}")

def test_get_stats_invalid_stat(mock_db):
    try:
        payload = {
            "sensor_id": ["1"],
            "metrics": ["Temperature"],
            "stats": "median"  # invalid
        }
        response = client.post("/sensorapi/query/", json=payload)
        logging.info("Invalid Stat Response: %s", response.json())
        assert response.status_code == 400
        assert "Invalid stat type" in response.json()["detail"]
        logging.info("test_get_stats_invalid_stat passed Successfully")

    except Exception as e:
        pytest.fail(f"Error in test_get_stats_invalid_stat: {e}")