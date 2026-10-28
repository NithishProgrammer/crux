import os

from sqlalchemy import Column, ForeignKey, String, create_engine , Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# "+psycopg2" tells SQLAlchemy which driver to use (the one in requirements.txt)
SQLALCHEMY_DATABASE_URL = "sqlite:///./crux.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All table classes inherit from this
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "User"

    userid = Column(String, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)  # stores the bcrypt hash, never the plain password


class Problems(Base):
    __tablename__ = "Problems"

    userid = Column(String, ForeignKey("User.userid"))
    problem_ID = Column(Integer, primary_key=True, index=True)
    problem = Column(String)
    sector = Column(String)  # stores the bcrypt hash, never the plain password


class Solutions(Base):
    __tablename__ = "Solutions"

    sol_id = Column(String , primary_key=True)
    userid = Column(String)
    problem_ID = Column(Integer, index=True)
    solution = Column(String)
    

def init_db():
    """Create the tables. Called when the server starts (not at import time)."""
    Base.metadata.create_all(bind=engine)
