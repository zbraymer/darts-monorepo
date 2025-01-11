from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./backend/data/dart.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Test connection
try:
    connection = engine.connect()
    print("Database connection successful!")
except Exception as e:
    print(f"Error: {e}")
