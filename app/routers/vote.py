from fastapi import APIRouter, Depends, status, HTTPException, responses
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):

    if vote.direction == 1:
        db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
        )
