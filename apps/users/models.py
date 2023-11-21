class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(Users))
    fullname = Column(String)
    login = Column(String)
    password = Column(String)

class UserLog(Base):
    __tablename__ = "userlog"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
