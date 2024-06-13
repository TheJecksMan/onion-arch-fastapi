from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from domain.schemas.notes import Category, CategoryWithID
from services.category_service import CategoryService

from infrastructure.database.engine import sqlalchemy_helper
from infrastructure.repositories.category_repository import SQLAlchemyCategoryRepository

router = APIRouter()

QueryIntID = Annotated[int, Query(ge=1, le=2147483647)]
QueryIntLimit = Annotated[int, Query(ge=1, le=50)]

Session = Annotated[AsyncSession, Depends(sqlalchemy_helper.session_getter)]


@router.post("/create")
async def create_caregory(
    schema: Category,
    sesssion: Session,
):
    repository = SQLAlchemyCategoryRepository(sesssion)
    return await CategoryService(repository).create(schema)


@router.put("/edit")
async def edit_caregory(
    schema: CategoryWithID,
    sesssion: Session,
):
    repository = SQLAlchemyCategoryRepository(sesssion)
    return await CategoryService(repository).edit(schema)


@router.get("/list")
async def get_all_categories(
    limit: QueryIntLimit,
    start_id: QueryIntID,
    sesssion: Session,
):
    repository = SQLAlchemyCategoryRepository(sesssion)
    return await CategoryService(repository).get_all(limit, start_id)


@router.delete("/delete")
async def delete_caregory(id: QueryIntID, sesssion: Session):
    repository = SQLAlchemyCategoryRepository(sesssion)
    result = await CategoryService(repository).remove(id)
    if result is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uncorrect ID")
    return result
