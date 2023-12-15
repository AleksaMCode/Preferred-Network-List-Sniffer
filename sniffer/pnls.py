import uvicorn

from settings import SERVER
from services import pub_sub

from pathlib import Path
from logger import create_logger
from fastapi import FastAPI

create_logger(f"{Path(__file__).stem}.log")
app = FastAPI()
app.include_router(pub_sub.router)

if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host=SERVER["localhost"],
        port=SERVER["port"],
        reload=True,
    )
