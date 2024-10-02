from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router, land_router
from auth_routes import auth_router
import models
from db import engine

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)
app.include_router(land_router)

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, replace with specific domain for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)