import orjson

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    class Config:

        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps

        arbitrary_types_allowed = True
