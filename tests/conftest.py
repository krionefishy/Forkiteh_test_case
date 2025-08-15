import pytest
from httpx import AsyncClient
from app.api.app import Application
from app.repository.database import Database
from app.utils.config import setup_config
from app.utils.store import Store
from app.utils.services import Service
from app.services.tron_service.tron_service import TronService
from app.services.routes_service.routes_service import RouteService


settings = setup_config("config.yaml")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    app_instance = Application()
    app_instance.db = Database()
    app_instance.settings = settings

    app_instance.store = Store(app_instance)
    app_instance.service = Service(app_instance)
    app_instance.service.tron_service = TronService(app_instance)
    app_instance.service.route_service = RouteService(app_instance)

    app_instance.app.state.db = app_instance.db
    app_instance.app.state.store = app_instance.store
    app_instance.app.state.service = app_instance.service

    async with AsyncClient(app=app_instance.app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def db():
    database = Database()
    await database.connect(settings.DATABASE_URL)
    yield database
    await database.disconnect()


@pytest.fixture
def mock_app():
    app = Application()
    app.db = Database()
    app.settings = settings

    app.store = Store(app)
    app.service = Service(app)
    app.service.tron_service = TronService(app)
    app.service.route_service = RouteService(app)

    app.app.state.db = app.db
    app.app.state.store = app.store
    app.app.state.service = app.service

    return app