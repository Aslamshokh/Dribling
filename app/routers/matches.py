from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Match, MatchPlayer, User
from app.schemas import Match as MatchSchema, MatchCreate
from app.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=List[MatchSchema])
async def get_matches(
        city: Optional[str] = Query(None, description="Filter by city"),
        format: Optional[str] = Query(None, description="Filter by format"),
        date: Optional[str] = Query(None, description="Filter by date"),
        status: Optional[str] = Query("open", description="Filter by status"),
        limit: int = Query(50, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all matches with filters"""
    query = db.query(Match)

    if city:
        query = query.filter(Match.city == city)
    if format:
        query = query.filter(Match.format == format)
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d")
            next_date = filter_date + timedelta(days=1)
            query = query.filter(and_(
                Match.date_time >= filter_date,
                Match.date_time < next_date
            ))
        except:
            pass
    if status:
        query = query.filter(Match.status == status)

    matches = query.order_by(Match.date_time).limit(limit).all()

    # Add players count
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
            "latitude": match.latitude,
            "longitude": match.longitude,
            "created_at": match.created_at,
            "players_count": len(match.players)
        }
        result.append(MatchSchema.model_validate(match_dict))

    return result


@router.post("/", response_model=MatchSchema)
async def create_match(
        match: MatchCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Create a new match"""
    db_match = Match(
        **match.model_dump(),
        created_by=current_user.id,
        status="open"
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    # Auto-join creator
    match_player = MatchPlayer(
        match_id=db_match.id,
        user_id=current_user.id
    )
    db.add(match_player)
    db.commit()

    # Add players count
    match_dict = db_match.__dict__
    match_dict['players_count'] = 1

    return MatchSchema.model_validate(match_dict)


@router.get("/{match_id}")
async def get_match(
        match_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get match details"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Get players with user info
    players = []
    for mp in match.players:
        user = db.query(User).filter(User.id == mp.user_id).first()
        if user:
            players.append({
                "id": mp.id,
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "username": user.username,
                    "photo_url": user.photo_url,
                    "rating": user.rating
                },
                "team": mp.team,
                "joined_at": mp.joined_at
            })

    # Get creator info
    creator = db.query(User).filter(User.id == match.created_by).first()

    return {
        "id": match.id,
        "title": match.title,
        "stadium": match.stadium,
        "city": match.city,
        "date_time": match.date_time,
        "format": match.format,
        "max_players": match.max_players,
        "status": match.status,
        "latitude": match.latitude,
        "longitude": match.longitude,
        "created_at": match.created_at,
        "creator": {
            "id": creator.id,
            "first_name": creator.first_name,
            "username": creator.username,
            "photo_url": creator.photo_url
        } if creator else None,
        "players": players,
        "players_count": len(players)
    }


@router.post("/{match_id}/join")
async def join_match(
        match_id: int,
        team: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Join a match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.status not in ["open", "full"]:
        raise HTTPException(status_code=400, detail="Match is not available for joining")

    # Check if already joined
    existing = db.query(MatchPlayer).filter(
        and_(
            MatchPlayer.match_id == match_id,
            MatchPlayer.user_id == current_user.id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already joined this match")

    # Check max players
    if len(match.players) >= match.max_players:
        match.status = "full"
        db.commit()
        raise HTTPException(status_code=400, detail="Match is full")

    # Join match
    match_player = MatchPlayer(
        match_id=match_id,
        user_id=current_user.id,
        team=team
    )
    db.add(match_player)

    # Update match status if full
    if len(match.players) + 1 >= match.max_players:
        match.status = "full"

    db.commit()

    return {"message": "Successfully joined the match", "success": True}


@router.post("/{match_id}/leave")
async def leave_match(
        match_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Leave a match"""
    match_player = db.query(MatchPlayer).filter(
        and_(
            MatchPlayer.match_id == match_id,
            MatchPlayer.user_id == current_user.id
        )
    ).first()

    if not match_player:
        raise HTTPException(status_code=404, detail="Not joined this match")

    # Check if user is creator
    match = db.query(Match).filter(Match.id == match_id).first()
    if match and match.created_by == current_user.id:
        # If creator leaves, delete the match
        db.delete(match)
        db.commit()
        return {"message": "Match deleted", "success": True}

    db.delete(match_player)

    # Update match status
    if match and match.status == "full":
        match.status = "open"

    db.commit()

    return {"message": "Successfully left the match", "success": True}


@router.get("/cities/list")
async def get_cities():
    """Get list of available cities"""
    return {"cities": settings.CITIES}