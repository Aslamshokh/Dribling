from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from datetime import datetime 
 
app = FastAPI( 
    title="Dribbling API", 
    description="Backend for Dribbling football platform", 
    version="1.0.0" 
) 
 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 
 
@app.get("/") 
async def root(): 
    return { 
        "message": "Welcome to Dribbling API", 
        "version": "1.0.0", 
        "docs": "/docs" 
    } 
 
@app.get("/api/health") 
async def health_check(): 
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()} 
