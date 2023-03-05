from games import models, schemas


def get_game(game_id: int):
    return models.Game.filter(models.Game.id == game_id).first()


def get_games(skip: int = 0, limit: int = 100):
    return list(models.Game.select().offset(skip).limit(limit))


def create_game(game: schemas.GameBase):
    db_game = models.Game(name=game.name,
                          description=game.description,
                          publication_date=game.publication_date,
                          status=True,
                          developer=game.developer_id
                          )
    db_game.save()
    return db_game
