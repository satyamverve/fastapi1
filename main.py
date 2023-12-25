# main.py

from fastapi import FastAPI
from app.modules.users.users_routes import router as users_router
from app.modules.posts.posts_routes import router as posts_router
from app.auth.auth import router as auth_router
from app.config.database import engine
from app.models.user_tables import Base as UserBase
from app.models.posts_table import Base as PostBase
from app.models.votes_table import Base as VoteBase
from app.modules.voting.vote import router
from fastapi.middleware.cors import CORSMiddleware

UserBase.metadata.create_all(bind=engine)
PostBase.metadata.create_all(bind=engine)
VoteBase.metadata.create_all(bind=engine)



app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

origins=["*"]   # ["*"] this value make the API public on any domain, assign the value accordingly  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "This is the root path"}

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(router, prefix="/votes", tags=["Voting"])