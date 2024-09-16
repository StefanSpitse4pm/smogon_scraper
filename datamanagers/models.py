from sqlalchemy import TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Pokemon(Base):
    __tablename__ = "pokemon"
    id: Mapped[int] = mapped_column(primary_key=True)
    pokemon_name: Mapped[str] = mapped_column(VARCHAR)
    pokemon_set: Mapped[str] = mapped_column(TEXT)
    format: Mapped[str] = mapped_column(VARCHAR)
    gen: Mapped[str] = mapped_column(VARCHAR)
