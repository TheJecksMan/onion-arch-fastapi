from typing import Any

from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update

from .abc import AbstarctRepository
from domain.models.notes import Notes, CategoriesNotes


class SQLAlchemyNotesRepository(AbstarctRepository):
    """
    SQLAlchemy repository implementation for Notes.

    This class provides methods to CRUD notes using SQLAlchemy
    with asynchronous support.
    """

    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, instance: dict[str, Any]):
        """Creates a new note with the provided data."""

        category_ids = instance.pop("categories")

        smt = insert(Notes).values(instance).returning(Notes.id)
        result = await self.session.execute(smt)
        note_id = result.scalar_one()

        if category_ids:
            associations = [
                {"note_id": note_id, "category_id": category_id} for category_id in category_ids
            ]
            smt = insert(CategoriesNotes).values(associations)
            await self.session.execute(smt)
        return note_id

    async def get(self, id: int):
        """Retrieves a note by its ID."""

        smt = select(Notes).where(Notes.id == id).options(joinedload(Notes.categories))
        result = await self.session.scalars(smt)
        return result.first()

    async def get_all(self, limit: int, start_id: int):
        """Retrieves all notes starting from a specific ID with a limit."""

        smt = (
            select(Notes)
            .where(Notes.id >= start_id)
            .order_by(Notes.id.asc())
            .limit(limit)
            .options(joinedload(Notes.categories))
        )
        result = await self.session.scalars(smt)
        return result.unique().all()

    async def edit(self, instance: dict[str, Any], id: int):
        """Updates an existing note with the provided data."""

        category_ids = instance.pop("categories", None)
        smt = update(Notes).values(**instance).where(Notes.id == id).returning(Notes)
        result = await self.session.scalars(smt)
        note = result.first()

        if category_ids and note:
            smt = delete(CategoriesNotes).where(CategoriesNotes.note_id == note.id)
            await self.session.execute(smt)

            associations = [
                {"note_id": note.id, "category_id": category_id} for category_id in category_ids
            ]
            smt = insert(CategoriesNotes).values(associations)
            await self.session.execute(smt)
        return note

    async def remove(self, id: int):
        """Deletes a note by its ID."""

        note = await self.session.get(Notes, id)
        if note:
            await self.session.delete(note)
            return True
        return False
