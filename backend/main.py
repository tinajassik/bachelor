from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes import geo
import os

from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(geo.router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)