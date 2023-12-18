#app.modeules/voting/vote_service

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.votes_table import Vote
from app.dto.vote_schema import VoteCreate
from app.oauth import oauth2
from app.models.posts_table import Post

def vote_user(db: Session, vote: VoteCreate, 
                current_user: int = Depends(oauth2.get_current_user)):
    
    #logic to test the post that is it exist on db or not
    post=db.query(Post).filter(Post.id==vote.v_post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.v_post_id} does not exist")
    
    
    vote_query = db.query(Vote).filter(Vote.v_post_id== vote.v_post_id, 
                              Vote.v_user_id == current_user.id)
    found_vote=vote_query.first()
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=
                        f"User {current_user.id} has already voted on post {vote.v_post_id}")
        new_vote=Vote(v_post_id= vote.v_post_id, v_user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added your vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {'message' : 'successfully deleted vote'}