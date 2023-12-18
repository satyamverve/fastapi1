#app/modeules/voting/vote.py

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.oauth import oauth2
from app.dto.vote_schema import VoteCreate
from app.config.database import get_db
from app.modules.voting.vote_service import vote_user

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: VoteCreate, db: Session= Depends(get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    return vote_user(db,vote,current_user)
            