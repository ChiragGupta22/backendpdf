from sqlalchemy import Column, String,Integer,DateTime,Boolean
from src.database.database import Base

class UserModel(Base):

  __tablename__ = "users"

  id = Column(Integer,primary_key=True)
  username = Column(String)
  email = Column(String , nullable=False)
  password = Column(String,nullable=False)