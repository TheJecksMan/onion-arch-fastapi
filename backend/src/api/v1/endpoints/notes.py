from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.notes import CreateNote, NoteWithID, EditNote
from services.notes_service import NotesService

from infrastructure.database.engine import sqlalchemy_helper
from infrastructure.repositories.notes_repository import SQLAlchemyNotesRepository

router = APIRouter()

QueryIntID = Annotated[int, Query(ge=1, le=2147483647)]
QueryIntLimit = Annotated[int, Query(ge=1, le=50)]

Session = Annotated[AsyncSession, Depends(sqlalchemy_helper.session_getter)]


@router.post("/create")
async def create_note(
    schema: CreateNote,
    sesssion: Session,
):
    repository = SQLAlchemyNotesRepository(sesssion)
    return await NotesService(repository).create(schema)


@router.put("/edit")
async def edit_note(
    schema: EditNote,
    sesssion: Session,
):
    repository = SQLAlchemyNotesRepository(sesssion)
    return await NotesService(repository).edit(schema)


@router.get("/", response_model=NoteWithID)
async def get_note(
    id: QueryIntID,
    sesssion: Session,
):
    repository = SQLAlchemyNotesRepository(sesssion)
    return await NotesService(repository).get(id)


@router.get("/list", response_model=list[NoteWithID])
async def get_all_notes(
    limit: QueryIntLimit,
    start_id: QueryIntID,
    sesssion: Session,
):
    repository = SQLAlchemyNotesRepository(sesssion)
    return await NotesService(repository).get_all(limit, start_id)


@router.delete("/delete")
async def delete_note(
    id: QueryIntID,
    sesssion: Session,
):
    repository = SQLAlchemyNotesRepository(sesssion)
    result = await NotesService(repository).remove(id)
    if result is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uncorrect ID")
    return result
