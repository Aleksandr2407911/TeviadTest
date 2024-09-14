from typing import AsyncGenerator
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from src.api.auth import verify_credentials
from src.db.db import get_db
from src.api.router import router
from fastapi.middleware.cors import CORSMiddleware
from src.logs import setup_logging
from src.db import settings


#setup_logging(settings)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    get_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="TevianTest",
    description="API for TevianTest",
    version="1.0.0",
    #dependencies=[Depends(verify_credentials)]
)
app.include_router(router)

origins = ["http://localhost:8000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.dependencies.append(Depends(verify_credentials))
