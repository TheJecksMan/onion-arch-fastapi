from infrastructure.repositories.abc import AbstarctRepository


class NotesService:
    """
    Service class for managing notes.

    This class provides methods to create, edit, retrieve all, and remove notes
    using a repository pattern, allowing for dependency inversion.
    """

    def __init__(self, repository: AbstarctRepository) -> None:
        self.repository = repository

    async def create(self, schema):
        param = schema.model_dump()
        return await self.repository.create(param)

    async def edit(self, schema):
        param = schema.model_dump(exclude_none=True)
        note_id = param.pop("id")
        return await self.repository.edit(param, note_id)

    async def get_all(self, limit: int, start_id: int):
        return await self.repository.get_all(limit, start_id)

    async def remove(self, id: int):
        return await self.repository.remove(id)

    async def get(self, id: int):
        return await self.repository.get(id)
