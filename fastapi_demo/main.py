from os import getenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_demo.competitors.competitors_store import CompetitorsStore
from fastapi_demo.competitors.competitor import Competitor, RegistrationModel

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app = FastAPI(
    title="BeastyBeastServer",
    version="0.0.1",
    description="A game to test your application making skills!"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/web", StaticFiles(directory="fastapi_demo/static", html=True), name="static")

db_port = getenv("BB_DB_PORT")
if db_port is not None:
    competitor_store = CompetitorsStore(port=int(db_port))
else:
    competitor_store = CompetitorsStore()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/competitors/")
def read_item():
    return competitor_store.get_competitors()

@app.delete("/competitors/{id}")
def read_item(id: str):
    competitor_store.delete_competitor(id)

@app.post("/competitors/")
def read_item(registration: RegistrationModel):
    return competitor_store.store_competitor(registration.dict())