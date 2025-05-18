from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes import geo
import os
from data import data_access 

from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("main.py: FastAPI application starting up (startup_event)...")
    app_data_dir = 'app/data'
    print(f"main.py: Startup event: Ensuring directory '{app_data_dir}' exists.")
    if not os.path.exists(app_data_dir):
        try:
            os.makedirs(app_data_dir, exist_ok=True)
            print(f"main.py: Startup event: Directory '{app_data_dir}' created/ensured.")
        except Exception as e:
            print(f"main.py: Startup event: Error creating directory '{app_data_dir}': {e}")
    else:
        print(f"main.py: Startup event: Directory '{app_data_dir}' already exists.")

    print("main.py: Startup event: Calling data_access.create_hdf5_file().")
    data_access.create_hdf5_file()
    print("main.py: Startup event: Call to data_access.create_hdf5_file() completed.")
    print("main.py: FastAPI application startup complete (end of startup_event).")

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
