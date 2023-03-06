from auth import models, schemas
from auth.utils import get_hashed_password


def get_user(username: str):
    return models.User.filter(models.User.username == username).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_admin(user: schemas.UserCreate):
    db_user = models.User(username=user.username,
                          first_name=user.first_name,
                          last_name=user.last_name,
                          password=get_hashed_password(user.password))
    db_user.save()
    return db_user
