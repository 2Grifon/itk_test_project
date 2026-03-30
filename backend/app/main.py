from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi_pagination import add_pagination

# TODO: import all models here to ensure they are registered with SQLAlchemy

from app.core.config import settings

app = FastAPI(
    title="Template project API",  # TODO изменить название
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

# main_router.include_router()  # TODO подключить роутеры

app.include_router(main_router)

# add_pagination(app) #TODO подключить пагинациб при необходимости
