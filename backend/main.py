from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_routes import geo

app = FastAPI()
app.include_router(geo.router, prefix="/api/geo")

@app.get("/")
def read_root():
    return {"message": "Backend Up and Running! :)"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)