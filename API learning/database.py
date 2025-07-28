from sqlalchemy import create_engine, Column, Integer, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests

Base = declarative_base()

class APIResponse(Base):
    __tablename__ = "api_responses"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)

# SQLite
engine = create_engine("sqlite:///api_data.db")
# PostgreSQL
# engine = create_engine("postgresql://user:password@localhost/dbname")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_api_response(endpoint_data):
    """Save API response to database"""
    session = Session()
    try:
        new_entry = APIResponse(data=endpoint_data)
        session.add(new_entry)
        session.commit()
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False
    finally:
        session.close()
def get_data():
    session = Session()
    try:
        data = session.query(APIResponse).all()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        session.close()

def clear_data():
    session = Session()
    try:
        session.query(APIResponse).delete()
        session.commit()
    except Exception as e:
        print(f"Error clearing data: {e}")


    