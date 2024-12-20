from pydantic import BaseModel, Field

import settings
import database
from api.schemas import StayForgeModel
from repository import MongoRepository

from faker import Faker

collection_name = 'key'

key_repository = MongoRepository(
    database=settings.DATABASE_NAME,
    collection=collection_name,
    client=database.client
)

faker = Faker('ja_JP')


class KeyInput(BaseModel):
    name: str = Field(
        ...,
        examples=[f"ホテルステイフォージ{faker.town()}"],
        description="The name of the hotel key. By default, it combines a base name with a random town."
    )
    postcode: str = Field(
        "000-0000",
        examples=[faker.postcode()],
        description="The postal code of the key location."
    )
    address: str = Field(
        "000-0000",
        examples=[
            f"{faker.administrative_unit()}{faker.city()}{faker.town()}{faker.chome()}{faker.ban()}{faker.gou()}"
        ],
        description="The full effective of the key, including administrative unit, city, town, and detailed location."
    )
    telephone: str = Field(
        examples=[f"{faker.phone_number()}"],
        description="The contact telephone number for the key."
    )


class Key(KeyInput, StayForgeModel):
    pass
