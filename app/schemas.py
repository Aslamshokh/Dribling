from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: str
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    rating: int
    matches_played: int
    wins: int
    losses: int
    created_at: datetime

    class Config:
        from_attributes = True


class MatchBase(BaseModel):
    title: str
    stadium: str
    city: str = "Пенджикент"
    date_time: datetime
    format: str
    max_players: int
    latitude: Optional[float] = 39.4952
    longitude: Optional[float] = 67.6093


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    status: str
    created_by: int
    created_at: datetime
    players_count: Optional[int] = 0

    class Config:
        from_attributes = True


class MatchPlayerBase(BaseModel):
    match_id: int
    user_id: int
    team: Optional[str] = None


class MatchPlayerCreate(MatchPlayerBase):
    pass


class MatchPlayer(MatchPlayerBase):
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True