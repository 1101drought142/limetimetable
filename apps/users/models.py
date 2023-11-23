import enum

from sqlalchemy import  Column, Integer, String, Text, ForeignKey, Enum

from database import Base

class Users(enum.Enum):
    api = 0
    manager = 1 
    superuser = 2
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(Users))
    fullname = Column(String)
    login = Column(String)
    password = Column(String)

    def is_admin(self) -> bool:
        if self.type == Users.superuser:
            return True
        return False

class UserLog(Base):
    __tablename__ = "userlog"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)

class Logins(Base):
    __tablename__ = "logins"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))