from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine,    Base
from app.routers import user, post, auth, vote
from pydantic import BaseSettings
from app import config

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com",# people from google.com can talk to us now
           "https://www.youtube.com"
]


app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"], # which http methods are allowed
                   allow_headers=["*"]) # which headers are allowed


@app.get("/")
def start_response():
    return {"hello":"world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)