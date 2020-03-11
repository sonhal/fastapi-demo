from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from fastapi_demo.users import UserStore

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/web", StaticFiles(directory="fastapi_demo/static", html=True), name="static")


userstore = UserStore()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users")
def read_item():
    return userstore.get_users()


class User(BaseModel):
    name: str
    age: int
    type: str = "basic"


@app.post("/users/")
def read_item(user: User):
    return userstore.add_user(user.name, user.age, user.type)