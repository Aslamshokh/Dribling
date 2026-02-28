@echo off
mkdir app
mkdir app\routers

echo. > app\__init__.py
echo. > app\routers\__init__.py

echo from fastapi import FastAPI > app\main.py
echo from fastapi.middleware.cors import CORSMiddleware >> app\main.py
echo from datetime import datetime >> app\main.py
echo. >> app\main.py
echo app = FastAPI( >> app\main.py
echo     title="Dribbling API", >> app\main.py
echo     description="Backend for Dribbling football platform", >> app\main.py
echo     version="1.0.0" >> app\main.py
echo ) >> app\main.py
echo. >> app\main.py
echo app.add_middleware( >> app\main.py
echo     CORSMiddleware, >> app\main.py
echo     allow_origins=["*"], >> app\main.py
echo     allow_credentials=True, >> app\main.py
echo     allow_methods=["*"], >> app\main.py
echo     allow_headers=["*"], >> app\main.py
echo ) >> app\main.py
echo. >> app\main.py
echo @app.get("/") >> app\main.py
echo async def root(): >> app\main.py
echo     return { >> app\main.py
echo         "message": "Welcome to Dribbling API", >> app\main.py
echo         "version": "1.0.0", >> app\main.py
echo         "docs": "/docs" >> app\main.py
echo     } >> app\main.py
echo. >> app\main.py
echo @app.get("/api/health") >> app\main.py
echo async def health_check(): >> app\main.py
echo     return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()} >> app\main.py

echo Проект создан!