from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.schemas.common import ErrorResponse


class AppException(Exception):
    """Base application exception carrying an HTTP status code and detail message."""

    status_code: int = 500
    code: str | None = None

    def __init__(self, detail: str, code: str | None = None) -> None:
        self.detail = detail
        if code is not None:
            self.code = code
        super().__init__(detail)


class NotFoundError(AppException):
    status_code = 404
    code = "not_found"


class ConflictError(AppException):
    status_code = 409
    code = "conflict"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail, code=exc.code).model_dump(),
        )
