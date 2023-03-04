from typing import Union, List
from fastapi import FastAPI, Depends, HTTPException
import crud, database, models, schemas
from database import db_state_default

sleep_time = 10

database.db.connect()
database.db.create_tables([models.Game, models.Developer])
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


@app.post("/games/", response_model=schemas.GameBase, dependencies=[Depends(get_db)])
def create_game(game: schemas.GameBase):
    developer = crud.get_developer(developer_id=game.developer_id)
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    return crud.create_game(game=game)

@app.get("/games/", response_model=List[schemas.GameBase], dependencies=[Depends(get_db)])
def list_game(skip: int = 0, limit: int = 100):
    games = crud.get_games(skip=skip, limit=limit)
    return games


@app.post("/developers/", response_model=schemas.DeveloperBase, dependencies=[Depends(get_db)])
def create_developer(developer: schemas.DeveloperBase):
    return crud.create_developer(developer=developer)


@app.get("/developers/", response_model=List[schemas.DeveloperBase], dependencies=[Depends(get_db)])
def list_developer(skip: int = 0, limit: int = 100):
    developers = crud.get_developers(skip=skip, limit=limit)
    return developers
