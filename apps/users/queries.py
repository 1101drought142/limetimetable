from sqlalchemy.orm import Session

from apps.users.models import User, UserLog

def get_user_or_None(db: Session, username, password) -> User|None:
    user = db.query(User).filter(User.login == username, User.password == password).first()
    return user

def create_log(db, user_id, action):
    db.add(UserLog(user=user_id, text=action))
    db.commit()