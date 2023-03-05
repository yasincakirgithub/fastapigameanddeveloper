from developers import models,schemas

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


