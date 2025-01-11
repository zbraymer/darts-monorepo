from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DATABASE_URL = "sqlite:///../data/dart.db"  # Relative path to the database file
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

# Define the players table
players = Table(
    "players",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

