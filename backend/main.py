from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import routers
from database import Base, engine
from models import models


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Server is running"}


for router in routers:
    app.include_router(router)