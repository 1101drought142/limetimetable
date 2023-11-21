from sqlalchemy.orm import Session

from apps.users.models import User

def get_user_or_None(db: Session, username, password) -> User|None:
    user = db.query(User).filter(User.login == username, User.password == password).first()
    return user