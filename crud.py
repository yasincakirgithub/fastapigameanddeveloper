import models, schemas


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


def get_developer(developer_id: int):
    return models.Developer.filter(models.Developer.id == developer_id).first()


def get_developers(skip: int = 0, limit: int = 100):
    return list(models.Developer.select().offset(skip).limit(limit))


def create_developer(developer: schemas.DeveloperBase):
    db_developer = models.Developer(username=developer.username,
                                    full_name=developer.full_name,
                                    age=developer.age)
    db_developer.save()
    return db_developer
