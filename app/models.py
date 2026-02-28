from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    photo_url = Column(String, nullable=True)
    rating = Column(Integer, default=0)
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    created_matches = relationship("Match", back_populates="creator", foreign_keys="Match.created_by")
    match_participations = relationship("MatchPlayer", back_populates="user")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    stadium = Column(String)
    city = Column(String, default="Пенджикент")
    date_time = Column(DateTime)
    format = Column(String)  # 5x5, 7x7, 11x11
    max_players = Column(Integer)
    status = Column(String, default="open")  # open, full, finished, cancelled
    created_by = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, default=39.4952)
    longitude = Column(Float, default=67.6093)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="created_matches", foreign_keys=[created_by])
    players = relationship("MatchPlayer", back_populates="match", cascade="all, delete-orphan")


class MatchPlayer(Base):
    __tablename__ = "match_players"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    team = Column(String, nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    match = relationship("Match", back_populates="players")
    user = relationship("User", back_populates="match_participations")