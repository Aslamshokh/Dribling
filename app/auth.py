from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import hmac
import hashlib
import json
from typing import Optional
from app.database import get_db
from app.models import User
from app.config import settings


async def verify_telegram_auth(init_data: str) -> Optional[dict]:
    """Verify Telegram WebApp init data"""
    try:
        # Parse data
        data = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                data[key] = value

        if 'hash' not in data:
            return None

        hash_value = data['hash']
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash')

        # Create secret key
        secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()

        # Calculate hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if calculated_hash != hash_value:
            return None

        # Parse user data
        if 'user' in data:
            try:
                user_data = json.loads(data['user'])
                return user_data
            except:
                return None

        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return None


async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
) -> User:
    """Get current user from Telegram init data"""
    init_data = request.headers.get('X-Telegram-Init-Data')

    if not init_data:
        # Для разработки возвращаем тестового пользователя
        if settings.DEBUG:
            user = db.query(User).filter(User.telegram_id == 123456789).first()
            if not user:
                user = User(
                    telegram_id=123456789,
                    username="test_user",
                    first_name="Тестовый",
                    photo_url=None
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication data"
        )

    user_data = await verify_telegram_auth(init_data)

    if not user_data and not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data"
        )

    # Get or create user
    if user_data:
        user = db.query(User).filter(User.telegram_id == user_data['id']).first()

        if not user:
            user = User(
                telegram_id=user_data['id'],
                username=user_data.get('username'),
                first_name=user_data.get('first_name', ''),
                photo_url=user_data.get('photo_url')
            )
            db.add(user)
            db.commit()
            db.refresh(user)
    else:
        # Тестовый пользователь для разработки
        user = db.query(User).filter(User.telegram_id == 123456789).first()
        if not user:
            user = User(
                telegram_id=123456789,
                username="test_user",
                first_name="Тестовый",
                photo_url=None
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    return user