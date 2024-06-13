from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from .abc import AbstarctRepository
from domain.models.notes import Categories


class SQLAlchemyCategoryRepository(AbstarctRepository):
    """
    SQLAlchemy repository implementation for Categories.

    This class provides methods to CRUD categories using SQLAlchemy
    with asynchronous support.
    """

    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, instance: dict[str, Any]):
        """Creates a new category with the provided data."""

        smt = insert(Categories).values(**instance).returning(Categories.id)
        result = await self.session.scalars(smt)
        return result.first()

    async def get(self, id: int):
        """Retrieves a category by its ID."""

        smt = select(Categories).where(Categories.id == id)
        result = await self.session.scalars(smt)
        return result.first()

    async def get_all(self, limit: int, start_id: int):
        """Retrieves all categories starting from a specific ID with a limit."""

        smt = select(Categories).where(Categories.id >= start_id).limit(limit)
        result = await self.session.scalars(smt)
        return result.all()

    async def edit(self, instance: dict[str, Any], id: int):
        """Updates an existing category with the provided data."""

        smt = update(Categories).values(**instance).where(Categories.id == id).returning(Categories)
        result = await self.session.scalars(smt)
        return result.first()

    async def remove(self, id: int):
        """Updates an existing category with the provided data."""

        category = await self.session.get(Categories, id)
        if category:
            await self.session.delete(category)
            return True
        return False
