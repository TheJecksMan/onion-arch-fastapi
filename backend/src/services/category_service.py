from pydantic import BaseModel

from infrastructure.repositories.abc import AbstarctRepository


class CategoryService:
    """Service class for managing categories.

    This class provides methods to create, edit, retrieve all, and remove categories
    using a repository pattern, allowing for dependency inversion.
    """

    __slots__ = ("repository",)

    def __init__(self, repository: AbstarctRepository) -> None:
        self.repository = repository

    async def create(self, schema: BaseModel):
        param = schema.model_dump(exclude_none=True)
        return await self.repository.create(param)

    async def edit(self, schema: BaseModel):
        param = schema.model_dump(exclude_none=True)
        category_id = param.pop("id")
        return await self.repository.edit(param, category_id)

    async def get_all(self, limit: int, start_id: int):
        return await self.repository.get_all(limit, start_id)

    async def remove(self, id: int):
        return await self.repository.remove(id)
