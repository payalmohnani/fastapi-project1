from fastapi import FastAPI
from .database import engine
from . import models 
from .routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path operation app 
# @ -> Decorator that converts the function into Fast API function
# app -> name of the instance of FASTAPI
# get -> https request method to retrieve data
# the argument of get method is the address/URL/path from which the request can be made
# root is path operation function(any relevant name can be given) that gives the response to given request


@app.get("/")  
def root():
    return {"message": "Hello World"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)