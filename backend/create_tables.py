"""
Create all database tables
"""
from database import engine, Base
import models

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    print("Tables:", Base.metadata.tables.keys())

if __name__ == "__main__":
    create_tables()
