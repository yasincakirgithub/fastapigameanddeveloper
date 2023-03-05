from typing import Union, List
from fastapi import FastAPI, Depends, HTTPException

import database
from database import db_state_default

from developers import crud as developers_crud
from games import crud as games_crud

from developers import models as developer_models
from games import models as games_models

from developers import schemas as developer_schemas
from games import schemas as games_schemas




sleep_time = 10

database.db.connect()
database.db.create_tables([games_models.Game, developer_models.Developer])
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


@app.post("/games/", response_model=games_schemas.GameBase, dependencies=[Depends(get_db)])
def create_game(game: games_schemas.GameBase):
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
