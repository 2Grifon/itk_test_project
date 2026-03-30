from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi_pagination import add_pagination

from app.core.config import settings
from app.modules.wallet import models  # noqa: F401
from app.modules.wallet.routes import router as wallet_router

app = FastAPI(
    title="ITK test project API",
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

main_router = APIRouter(prefix="/api", tags=["API"])

main_router.include_router(wallet_router)

app.include_router(main_router)

# add_pagination(app) #TODO подключить пагинациб при необходимости
