from typing import Dict

import pokebase as pb
from pydantic import BaseModel, Field, PositiveInt


class Pokemon(BaseModel):

    name: str = Field(min_length=1, max_length=32)
    stats: Dict[str, int]
    level: int = Field(ge=0, le=100)
    typing: list[str] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.typing = list(
            map(lambda pokemon: str(pokemon.type), pb.pokemon(self.name).types)
        )


class iv(BaseModel):
    hp: int = Field(alias="iv_health", ge=0, le=31)
    atk: int = Field(alias="iv_attack", ge=0, le=31)
    spa: int = Field(alias="iv_special_attack", ge=0, le=31)
    deff: int = Field(alias="iv_defence", ge=0, le=31)
    spd: int = Field(alias="iv_special_defence", ge=0, le=31)
    spe: int = Field(alias="iv_speed", ge=0, le=31)


class ev(BaseModel):
    hp: int = Field(alias="ev_health", ge=0, le=255)
    atk: int = Field(alias="ev_attack", ge=0, le=255)
    spa: int = Field(alias="ev_special_attack", ge=0, le=255)
    deff: int = Field(alias="ev_defence", ge=0, le=255)
    spd: int = Field(alias="ev_special_defence", ge=0, le=255)
    spe: int = Field(alias="ev_speed", ge=0, le=255)


class ActiveStats(BaseModel):
    hp: PositiveInt = Field(alias="health")
    atk: PositiveInt = Field(alias="attack")
    spa: PositiveInt = Field(alias="special_attack")
    deff: PositiveInt = Field(alias="defence")
    spd: PositiveInt = Field(alias="special_defence")
    spe: PositiveInt = Field(alias="speed")

    @classmethod
    def calculate_stats(cls, pokemon: Pokemon, iv: iv, ev: ev) -> "ActiveStats":
        pb.pokemon()


t = Pokemon(name="venusaur", stats={"test": 23}, level=32)
print(t)
