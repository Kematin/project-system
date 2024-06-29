import uuid
from datetime import datetime
from typing import Any, List

from pydantic import UUID4
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    select,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

DATABASE_URL = config.DATABASE_URL
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
    bind=engine,
)
Base = declarative_base()


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class Project(Base):
    __tablename__ = "project"

    id = Column(
        "id",
        Text(length=36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
    )
    name = Column(String(length=70), unique=False)
    summary = Column(Text)
    price = Column(Integer)
    category = Column(Integer)
    have_presentation = Column(Boolean)
    have_product = Column(Boolean)
    have_unique = Column(Boolean)
    is_blocked = Column(Boolean, nullable=True, default=False)
    created_at = Column(DateTime, default=datetime.today)


class SqlAlchemyUoW:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def commit(self) -> None:
        try:
            await self._db.commit()
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err

    async def rollback(self) -> None:
        try:
            await self._db.rollback()
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err

    async def delete(self, instance) -> None:
        try:
            await self._db.delete(instance)
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err
        await self.commit()

    async def refresh(self, instance) -> None:
        await self.commit()
        try:
            await self._db.refresh(instance)
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err


class Database:
    def __init__(self, model: Base, db: AsyncSession):
        self._model = model
        self._db = db
        self._uow = SqlAlchemyUoW(db)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        items = await self._db.execute(select(self._model).offset(skip).limit(limit))
        return items.scalars().all()

    async def get(self, id: UUID4 | int) -> Any:
        item = await self._db.execute(
            select(self._model).filter(self._model.id == str(id))
        )
        if item:
            return item.scalars().first()
        else:
            return False

    async def create(self, data: dict) -> None:
        db_data = self._model(**data)
        self._db.add(db_data)
        await self._uow.refresh(db_data)
        return db_data.id

    async def delete(self, id: UUID4 | int) -> bool:
        item = await self.get(id)
        if not item:
            return False

        await self._uow.delete(item)
        return True

    async def delete_all(self) -> None:
        items = await self.get_all()
        for item in items:
            await self._uow.delete(item)

    async def update(self, id: UUID4 | int, data: dict) -> Any:
        db_item = await self.get(id)

        if not db_item:
            return False

        for key, value in data.items():
            if value is None:
                continue
            setattr(db_item, key, value)

        self._db.add(db_item)
        await self._uow.refresh(db_item)

        return db_item
