def get_user_or_None(db: Session, username, password) -> Users|None:
    user = db.query(user_models.User).filter(user_models.User.login == username, user_models.User.password == password).first()
    return user