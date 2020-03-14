from os import getenv

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config

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

config = Config(".env")
DATABASE_HOST = config('DATABASE_HOST', cast=str, default="localhost")
DATABASE_PORT = config('DATABASE_PORT', cast=int, default=32775)
logger.info(f"DB host: {DATABASE_HOST}, DB port: {DATABASE_PORT}")
competitor_store = CompetitorsStore(conn_string=DATABASE_HOST, port=DATABASE_PORT)


@app.on_event("startup")
async def startup_event():
    await competitor_store.setup_db()


@app.on_event("shutdown")
async def startup_event():
    await competitor_store.close_connection()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/competitors/")
async def read_item():
    return await competitor_store.get_competitors()


@app.delete("/competitors/{id}")
async def read_item(id: str):
    return await competitor_store.delete_competitor(id)


@app.post("/competitors/")
async def read_item(registration: RegistrationModel):
    return await competitor_store.register_competitor(registration)