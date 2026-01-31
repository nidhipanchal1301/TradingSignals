from app.data_access import user_repository

from app.core.security import hash_password, verify_password, create_access_token



def signup(user, db):
    existing = user_repository.get_user_by_email(db, user.email)
    if existing:
        raise Exception("Email already exists")
    hashed = hash_password(user.password)
    new_user = user_repository.create_user(db, user.email, hashed)
    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token}

def login(user, db):
    db_user = user_repository.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise Exception("Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token}
