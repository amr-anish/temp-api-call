from sqlalchemy.orm import Session
from sqlalchemy import Date, cast, func
from model import SensorData
from schema import SensorInput, SensorQuery

# This function is used to insert the sensor data and commit to db
# Data will be validated using the schema using pydantic lib
def insert_sensor_data(db: Session, data: SensorInput):
    new_entry = SensorData(**data.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

# here we are querying the data based on the 
# we can query using the sensor id , metrics and timestamp
#  in any combination including the statics
def query_stats(db: Session, query: SensorQuery):
    db_query = db.query(SensorData)

    if query.sensor_id:
            db_query = db_query.filter(SensorData.sensor_id.in_(query.sensor_id))

    if query.metrics:
        db_query = db_query.filter(SensorData.metric.in_(query.metrics))
    
    if query.start_date and query.end_date:
        db_query = db_query.filter(SensorData.timestamp.between(query.start_date, query.end_date))
    else:
        current_date = cast(func.date(func.now()), Date)
        db_query = db_query.filter(SensorData.timestamp.startswith(current_date))


    # we have inbuilt function in sql alchemy we are using that 
    # to calculate the statics of the metrics
    stats_funcs = {
        "average": func.avg,
        "min": func.min,
        "max": func.max,
        "sum": func.sum
    }

    # verifying option is valid or not for stats
    if query.stats not in stats_funcs:
        raise ValueError(f"Invalid stat type: {query.stats}. Supported types are: {', '.join(stats_funcs.keys())}")

    results = {}
    # here we are filtering the sensor data using metrics since we need that value 
    # to pass in the function
    for metric in query.metrics:

        # getting the stats function such as min , max, avg or sum
        stats_func = stats_funcs[query.stats]

        res = db_query.filter(SensorData.metric == metric)\
                      .with_entities(stats_func(SensorData.value)).scalar()
        results[metric] = res

    return results

def get_all_data(db: Session):
    # getting all the data from db and returning it
    return db.query(SensorData).all()