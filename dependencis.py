from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.verifyUtils import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    user_id = verify_token(token)
    print("前端传过来的Token:", token)
    if not user_id:
        raise HTTPException(status_code=401, detail="无效或过期的Token")

    return user_id.get("sub")
