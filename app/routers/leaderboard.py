from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models import User
from app.auth import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/")
async def get_leaderboard(
        limit: int = Query(100, ge=1, le=500),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get leaderboard sorted by rating"""
    users = db.query(User).order_by(
        User.rating.desc(),
        User.wins.desc(),
        User.matches_played.desc()
    ).offset(offset).limit(limit).all()

    result = []
    for i, user in enumerate(users, offset + 1):
        result.append({
            "rank": i,
            "id": user.id,
            "name": user.first_name,
            "username": user.username,
            "rating": user.rating,
            "matches": user.matches_played,
            "wins": user.wins,
            "losses": user.losses,
            "win_rate": round((user.wins / user.matches_played * 100) if user.matches_played > 0 else 0, 1)
        })

    # Get current user rank
    current_user_rank = db.query(func.count(User.id)).filter(
        User.rating > current_user.rating
    ).scalar() + 1 if current_user else 0

    return {
        "leaderboard": result,
        "total": db.query(func.count(User.id)).scalar(),
        "current_user_rank": current_user_rank,
        "current_user": {
            "id": current_user.id,
            "name": current_user.first_name,
            "rating": current_user.rating,
            "matches": current_user.matches_played
        } if current_user else None
    }