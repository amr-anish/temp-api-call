from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn

from schema import SensorInput, SensorQuery
from operation import insert_sensor_data, query_stats, get_all_data
from db_connection import session, engine, base

# Setting up the app and adding the base prefix

router = APIRouter(prefix="/sensorapi")

# Initialize the db session and yeilding it to use by the functions
def get_db():
    db_session = session()
    try:
        yield db_session
    finally:
        db_session.close()


# we can insert the data using this function
@router.post("/data/")
def add_data(data: SensorInput, db: Session = Depends(get_db)):
    return insert_sensor_data(db, data)

#  we can query data based on our condition 
@router.post("/query/")
def get_data(query: SensorQuery, db: Session =Depends(get_db)):
    try:
        return query_stats(db, query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# we can get all the data in the db using this
@router.get("/data/")
def get_data(db: Session = Depends(get_db)):
    return get_all_data(db)

app = FastAPI()
# add back the router to app after adding the endpoints and prefix
app.include_router(router)

if __name__ == "__main__":
    
    # initializing the db if not there it will create
    base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)