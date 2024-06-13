from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import settings


class AbstractDatabaseEngine(ABC):
    __slots__ = ()

    @abstractmethod
    async def dispose(self):
        raise NotImplementedError

    @abstractmethod
    async def session_getter(self):
        raise NotImplementedError


class SQLAlchemyHelper(AbstractDatabaseEngine):
    __slots__ = ("engine", "session")

    def __init__(self, url: str | None = None, **kwargs) -> None:
        # На каждый запущенный экземпляр приложения будет запущено
        # 15 подключений и 5 дополнительных в случае переполнения.
        # Подробнее о pool: https://docs.sqlalchemy.org/en/20/core/pooling.html
        self.engine = create_async_engine(
            url=url or settings.URL_DATABASE,
            echo=kwargs.get("echo", settings.DEBUG_MODE),
            pool_size=kwargs.get("pool_size", 5),
            max_overflow=kwargs.get("max_overflow", 10),
        )

        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session.begin() as session:
            yield session


sqlalchemy_helper = SQLAlchemyHelper()
