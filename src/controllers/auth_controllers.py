from src.schema.auth_schema import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.models.user import UserModel
from fastapi import HTTPException,status,Request,UploadFile,Response
from src.utils.constant.settings import settings
from pwdlib import PasswordHash
import jwt
from datetime import datetime,timedelta
from src.rag.chat import ask_question
from src.rag.database import create_vector_db
import os


password_hash = PasswordHash.recommended()




def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body: UserSchema, db: Session):

    is_user = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Email Address Already Exists"
        )

    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        username=body.username,
        email=body.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Register Successful",
        "id": new_user.id,
        "email": new_user.email,
       
    }

def login_user(body: LoginSchema, db: Session, response: Response):
    user = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Wrong Email")

    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong Password")

    exp_time = datetime.now() + timedelta(days=settings.EXP_TIME)

    token = jwt.encode(
        {
            "_id": user.id,
            "email": user.email,
            "exp": exp_time
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHAM
    )

    response.set_cookie(
    key="token",
    value=token,
    httponly=True,
    samesite="lax",
    secure=False,
    path="/",
    domain="localhost"
)

    return {"message": "Login Success"}


def is_authenticated(request: Request, db: Session):
    print("COOKIES:",request.cookies)
    token = request.cookies.get("token")

    if not token:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unathorized")

    data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHAM]
    )

    user_id = data.get("_id")
    exp_time = data.get("exp")

    current_time = datetime.now().timestamp()
    if current_time>exp_time:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unathorized")

    print(data)

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unathorized")


    return {
    "id": user.id,
    "username": user.username,
    "email": user.email

    }

def upload_pdf(file: UploadFile, user_id):

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    create_vector_db(file_path, user_id)

    return {
        "message": "PDF uploaded successfully"
    }



def chat_pdf(query, user_id):
    return ask_question(query, user_id)

def logout_user(response: Response):
    response.delete_cookie(
        key="token",
        httponly=True,
        samesite="lax",
        secure= False,
         path="/"
    )

    return {
        "message": "Logout Success"
    }