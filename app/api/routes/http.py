import logging
from fastapi import APIRouter, FastAPI
from starlette.requests import Request

# from main import logger

router = APIRouter()
app = FastAPI()
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url} {request.client.host}")
    print(f"Request: {request.method} {request.url} {request.client.host}")
    response = await call_next(request)
    return response


@router.get("/countries")
async def getCountries():
    return {"message": "success", "countries": []}


@router.get("/")
async def root():
    return {"message": "Hello World"}
