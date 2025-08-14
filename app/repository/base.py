import typing
from sqlalchemy.orm import DeclarativeBase
import logging

if typing.TYPE_CHECKING:
    from app.api.app import Application


class Base(DeclarativeBase):
    pass


class BaseAccessor:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = logging.getLogger("Accessor")

    async def connect(self):
        self.logger.info(f"Connecting {self.__class__.__name__}")
        try:
            await self._on_connect()
            self.logger.info(f"Successfully connected {self.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"Connection failed in {self.__class__.__name__}: {e}")
            raise

    async def disconnect(self):
        self.logger.info(f"Disconnecting {self.__class__.__name__}")
        try:
            await self._on_disconnect()
            self.logger.info(f"Successfully disconnected {self.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"Disconnection error in {self.__class__.__name__}: {e}")
            raise

    async def _on_connect(self):
        pass

    async def _on_disconnect(self):
        pass

class BaseService:
    def __init__(self, app: "Application"):
        self.app = app
        self.logger = logging.getLogger("Service")

    async def connect(self):
        self.logger.info(f"Connecting {self.__class__.__name__}")
        try:
            await self._on_connect()
            self.logger.info(f"Successfully connected {self.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"Connection failed in {self.__class__.__name__}: {e}")
            raise

    async def disconnect(self):
        self.logger.info(f"Disconnecting {self.__class__.__name__}")
        try:
            await self._on_disconnect()
            self.logger.info(f"Successfully disconnected {self.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"Disconnection error in {self.__class__.__name__}: {e}")
            raise

    async def _on_connect(self):
        pass

    async def _on_disconnect(self):
        pass