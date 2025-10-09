from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        # look up user by email (username field in OAuth2 form)
        user = db.query(models.User).filter(
            models.User.email == user_credentials.username).first()

        if not user:
            logger.info("login: user not found", extra={"email": user_credentials.username})
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        # verify password (do not log passwords)
        verified = utils.verify(user_credentials.password, user.password)
        logger.info("login: user found", extra={"email": user_credentials.username, "verified": verified})

        if not verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # re-raise FastAPI HTTP exceptions
        raise
    except Exception as e:
        # log unexpected exceptions for debugging, then return generic 500
        logger.exception("login: unexpected error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error during authentication")


