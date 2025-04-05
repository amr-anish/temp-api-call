from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

'''
In this file we are validating the input / query that is passed as request body

for Input we are validating all the mandatory values and time is optional
for querying time is optional and we have send other values in list[str] we can query in combination
stats function name in str
'''
class SensorInput(BaseModel):
    sensor_id: str
    metric: str 
    value: float
    timestamp: Optional[datetime] = None

class SensorQuery(BaseModel):
    sensor_id: List[str]
    metrics: List[str]
    stats: str  # average, min, max, sum
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
