from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# we are using this base as a the basemodel and initialization of db while launching
base = declarative_base()

# we are using sqlite for this assignment which small and easy to implement no db setup requried
DB_URL = "sqlite:///./sensor_db.db"

# we are creating engine and sesson using sql alchemy
engine = create_engine(DB_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    