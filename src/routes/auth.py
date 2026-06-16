from fastapi import APIRouter, Depends, status,Request,Response
from sqlalchemy.orm import Session
from fastapi import UploadFile, File

from src.schema.auth_schema import UserSchema,LoginSchema
from src.database.database import get_db
from src.controllers import auth_controllers

user_routes = APIRouter(prefix="/auth")

@user_routes.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: UserSchema, db: Session = Depends(get_db)):
    return auth_controllers.register(body, db)

@user_routes.post("/login")
def login(
    body: LoginSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    return auth_controllers.login_user(body, db, response)


@user_routes.get("/is_auth",status_code=status.HTTP_200_OK)
def is_auth(request:Request,db: Session = Depends(get_db)):
    return auth_controllers.is_authenticated(request,db)

@user_routes.post("/logout")
def logout(response: Response):
    return auth_controllers.logout_user(response)

# @user_routes.post("/upload")
# def upload(
#     request: Request,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     user = auth_controllers.is_authenticated(request, db)

#     return auth_controllers.upload_pdf(
#         file,
#         user["id"]
#     )

@user_routes.get("/chat")
def chat(
    query: str,
    request: Request,
    db: Session = Depends(get_db)
):
    user = auth_controllers.is_authenticated(request, db)

    return auth_controllers.chat_pdf(
        query,
        user["id"]
    )

@user_routes.get("/me")
def get_me(request: Request, db: Session = Depends(get_db)):
    return auth_controllers.is_authenticated(request, db)