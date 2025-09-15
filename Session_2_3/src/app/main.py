import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from fastapi import FastAPI
from app.core.db import Base, engine
from app.api import users, tasks
import uvicorn

# Create tables in dev (prod uses Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker")
app.include_router(users.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)