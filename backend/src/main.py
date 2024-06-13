from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.settings import settings

from api.v1.router import router

app = FastAPI(
    debug=settings.DEBUG_MODE,
    version="0.1.0",
    title="Onion architecture",
    redirect_slashes=False,
    default_response_class=ORJSONResponse,
)

app.include_router(router, prefix="/api")
