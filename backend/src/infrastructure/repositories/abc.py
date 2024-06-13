from abc import ABC, abstractmethod


class AbstarctRepository(ABC):
    __slots__ = ()

    @abstractmethod
    async def create(self, instance, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, limit: int, start_id: int):
        raise NotImplementedError

    @abstractmethod
    async def edit(self, instance, id):
        raise NotImplementedError

    @abstractmethod
    async def remove(self, id):
        raise NotImplementedError
