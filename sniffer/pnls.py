from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import create_logger, log_info
from services import pub_sub
from settings import SERVER

origins = ["*"]

# Create a logger.
create_logger(f"{Path(__file__).stem}.log")
app = FastAPI()

# Add router.
app.include_router(pub_sub.router)

# Add CORS middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
def shutdown():
    log_info("Server shut down.")


if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host=SERVER["localhost"],
        port=SERVER["port"],
        reload=True,
    )
