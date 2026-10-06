import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.schemas.common import ErrorResponse

logger = logging.getLogger(__name__)


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


class BadRequestError(AppException):
    status_code = 400
    code = "bad_request"


class PayloadTooLargeError(AppException):
    status_code = 413
    code = "payload_too_large"


class UnsupportedMediaTypeError(AppException):
    status_code = 415
    code = "unsupported_media_type"


class StorageUnavailableError(AppException):
    """Object storage (MinIO) could not serve the request."""

    status_code = 503
    code = "storage_unavailable"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(detail=exc.detail, code=exc.code).model_dump(),
        )

    # Catch-all so unexpected errors return a consistent ErrorResponse shape
    # instead of a bare 500. FastAPI's own handler already covers HTTPException
    # (and preserves structured details such as the readiness probe's dict).
    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail="Internal server error", code="internal_error").model_dump(),
        )
