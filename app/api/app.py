from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import setup_config, Settings
from contextlib import asynccontextmanager
from app.repository.database import Database
from app.utils.store import Store, setup_store
from app.utils.services import Service, setup_services
import logging
import asyncio


class Application:
    def __init__(self):
        self.app: FastAPI = FastAPI(title="Pet_Paws_service", lifespan=self.lifespan)
        self.db: Database = Database()
        self.store: Store | None = None
        self.service: Service | None = None
        self.settings: Settings = None 


        self._setup_routes()
        self._setup_middleware()

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


    def _setup_logging(self):
        logging.basicConfig(
            level=self.settings.LOGGING_LEVEL,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


    def _setup_routes(self):
        from app.api.endpoints.endpoints import router as wallet_routes
        self.app.include_router(wallet_routes)


    async def _on_startup(self):
        logger = logging.getLogger("main")
        logger.info("Service is starting")

        self.settings = setup_config(config_path="config.yaml")
        logger.info("Config setuped")
        self._setup_logging()
        setup_store(self)
        setup_services(self)
        
        await self.db.connect(self.settings.DATABASE_URL)
        self.app.state.db = self.db
        self.app.state.store = self.store
        self.app.state.service = self.service
    

    async def _on_shutdown(self):
        logger = logging.getLogger("main")
        logger.info("service is shutting down")

        await self.db.disconnect()


    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self._on_startup()
        yield
        await self._on_shutdown()


app = Application()


