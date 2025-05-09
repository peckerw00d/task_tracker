import factory
from factory.alchemy import SQLAlchemyModelFactory

from src.db.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")
