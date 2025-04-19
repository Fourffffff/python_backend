from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud.User as crud
import schemas.User as schemas

router = APIRouter()

@router.get("/users", response_model=list[schemas.UserOut])
def create_user(db: Session = Depends(get_db)):
     return crud.get_users(db)
