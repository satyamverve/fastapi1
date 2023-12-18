#app/dto/vote_schema.py

from pydantic import BaseModel, conint

class VoteCreate(BaseModel):
    v_post_id: int
    # dir means direction
    dir : conint(le=1) # that means the values of "dir" should be less that or equal to 1