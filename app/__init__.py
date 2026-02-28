from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    photo_url = Column(String, nullable=True)
    rating = Column(Integer, default=0)  # Считается по количеству игр
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    created_matches = relationship("Match", back_populates="creator")
    match_participations = relationship("MatchPlayer", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    stadium = Column(String)
    city = Column(String, default="Пенджикент")  # По умолчанию Пенджикент
    date_time = Column(DateTime)
    format = Column(String)  # 5x5, 7x7, 11x11
    max_players = Column(Integer)
    status = Column(String, default="open")  # open, full, finished, cancelled
    created_by = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, default=39.4952)  # Пенджикент по умолчанию
    longitude = Column(Float, default=67.6093)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="created_matches")
    players = relationship("MatchPlayer", back_populates="match", cascade="all, delete-orphan")

class MatchPlayer(Base):
    __tablename__ = "match_players"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    team = Column(String, nullable=True)  # A или B
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="players")
    user = relationship("User", back_populates="match_participations")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    captain_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    captain = relationship("User", foreign_keys=[captain_id])
    members = relationship("TeamMember", back_populates="team")

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")