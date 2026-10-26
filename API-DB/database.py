# filepath: database.py
import sqlalchemy
from sqlalchemy import Column, Float, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/crux"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base class (All our tables will "inherit" from this)
Base = declarative_base()

# 5. Define the "Messages" Table structure

class UserModel(Base):
    __tablename__ = "User"


    userid = Column(String, primary_key=True, index=True) # Unique ID
    username = Column(String)
    password = Column(String)

# This command tells SQLAlchemy to go find all models inheriting 
# from "Base" and create the tables in the database file.
Base.metadata.create_all(bind=engine)
