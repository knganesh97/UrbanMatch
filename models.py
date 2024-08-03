from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    interests = relationship("Interest",primaryjoin="User.id == Interest.user_id",cascade="all,delete-orphan")

class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    hobby = Column(String, index=True)

