from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Throw(Base):
    __tablename__ = "throws"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    radius = Column(Float, nullable=False)
    angle = Column(Float, nullable=False)
    target = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    mode = Column(String, nullable=False)
    darts_per_target = Column(Integer, nullable=False)
    current_target = Column(Integer, default=1)
    completed_targets = Column(String, nullable=True)  # Comma-separated list of targets
    throws = relationship("Throw", backref="game")
