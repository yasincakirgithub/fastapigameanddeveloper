from typing import List
from fastapi import FastAPI, status, Depends, HTTPException

import database
from database import db_state_default

from developers import crud as developers_crud
from games import crud as games_crud
from auth import crud as auth_crud

from developers import models as developer_models
from games import models as games_models
from auth import models as auth_models

from developers import schemas as developer_schemas
from games import schemas as games_schemas
from auth import schemas as auth_schemas

from auth.utils import verify_password, create_access_token, create_refresh_token,decode_token
from auth.deps import JWTBearer




sleep_time = 10
database.db.connect()
database.db.create_tables([games_models.Game, developer_models.Developer, auth_models.User])
database.db.close()

app = FastAPI()


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close

async def get_auth_user(payload: dict = Depends(JWTBearer())):
    auth_user = auth_crud.get_user(payload["sub"])
    return auth_user.get_dict()


@app.post("/register/", response_model=auth_schemas.UserList, dependencies=[Depends(get_db)])
def register(user: auth_schemas.UserCreate):
    exist_user = auth_crud.get_user(username=user.username)
    if exist_user:
        raise HTTPException(status_code=400, detail="User already exist")
    return auth_crud.create_admin(user=user)


@app.post('/login', response_model=auth_schemas.TokenSchema)
async def login(user: auth_schemas.UserLogin):
    exist_user = auth_crud.get_user(user.username)
    if exist_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = exist_user.password
    if not verify_password(user.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }


@app.get("/users/", response_model=List[auth_schemas.UserList], dependencies=[Depends(get_db)])
def list_admin(skip: int = 0, limit: int = 100):
    users = auth_crud.get_users(skip=skip, limit=limit)
    return users


@app.post("/games/", response_model=games_schemas.GameBase, dependencies=[Depends(get_db)])
def create_game(game: games_schemas.GameBase,auth_user: auth_schemas.UserList = Depends(get_auth_user)):
    developer = developers_crud.get_developer(developer_id=game.developer_id)
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    return games_crud.create_game(game=game)


@app.get("/games/", response_model=List[games_schemas.GameBase], dependencies=[Depends(get_db)])
def list_game(skip: int = 0, limit: int = 100):
    games = games_crud.get_games(skip=skip, limit=limit)
    return games


@app.post("/developers/", response_model=developer_schemas.DeveloperBase, dependencies=[Depends(get_db)])
def create_developer(developer: developer_schemas.DeveloperBase):
    return developers_crud.create_developer(developer=developer)


@app.get("/developers/", response_model=List[developer_schemas.DeveloperBase], dependencies=[Depends(get_db)])
def list_developer(skip: int = 0, limit: int = 100):
    developers = developers_crud.get_developers(skip=skip, limit=limit)
    return developers
