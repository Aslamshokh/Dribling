from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import User, Match, MatchPlayer
from app.schemas import User as UserSchema
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
        current_user: User = Depends(get_current_user)
):
    """Get current user info"""
    return current_user


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/matches")
async def get_user_matches(
        user_id: int,
        status: str = "all",
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get user's matches"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get matches where user participated
    participations = db.query(MatchPlayer).filter(
        MatchPlayer.user_id == user_id
    ).all()

    match_ids = [p.match_id for p in participations]
    query = db.query(Match).filter(Match.id.in_(match_ids)) if match_ids else db.query(Match).filter(False)

    if status != "all":
        query = query.filter(Match.status == status)

    matches = query.order_by(Match.date_time.desc()).all()

    result = []
    for match in matches:
        match_dict = {
            "id": match.id,
            "title": match.title,
            "stadium": match.stadium,
            "city": match.city,
            "date_time": match.date_time,
            "format": match.format,
            "max_players": match.max_players,
            "status": match.status,
            "created_by": match.created_by,
            "players_count": len(match.players)
        }
        result.append(match_dict)

    return result