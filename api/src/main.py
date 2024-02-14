

from exceptions import http_error_handler
from fastapi import FastAPI
from starlette.exceptions import HTTPException

src = FastAPI()

src.add_exception_handler(HTTPException, http_error_handler)
