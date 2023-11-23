from sqlalchemy.orm import Session

from apps.users.models import User, UserLog

def get_user_or_None(db: Session, username, password) -> User|None:
    user = db.query(User).filter(User.login == username, User.password == password).first()
    return user

def create_log(db : Session, user_id : int, action: str):
    db.add(UserLog(user=user_id, text=action))
    db.commit()

def get_logs(db: Session):
    return db.query(UserLog, User).join(User, User.id == UserLog.user).all()