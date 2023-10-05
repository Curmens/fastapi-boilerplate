from fastapi import FastAPI
from app.api.routes.http import router as api_router
import logging
from starlette.requests import Request

app = FastAPI()
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
app.include_router(api_router, prefix="/api")


async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url} {request.client.host}")
    print(f"Request: {request.method} {request.url} {request.client.host}")
    response = await call_next(request)
    return response
