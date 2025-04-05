from sqlalchemy import Column, Integer, Float, String, DateTime, func
from db_connection import base


# I have created a model class for the table sensor_data
class SensorData(base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True) # primary key
    sensor_id = Column(String(50), index=True)
    metric = Column(String(50)) 
    value = Column(Float) # value of the metric
    timestamp = Column(DateTime, default=func.now())
