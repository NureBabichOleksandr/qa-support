from typing import Any


class AppException(Exception):
    status_code: int = 400
    default_detail: str = "Bad request"

    def __init__(self, detail: str | None = None, *, extra: dict[str, Any] | None = None) -> None:
        self.detail = detail or self.default_detail
        self.extra = extra or {}
        super().__init__(self.detail)


class BadRequestException(AppException):
    status_code = 400
    default_detail = "Bad request"


class UnauthorizedException(AppException):
    status_code = 401
    default_detail = "Not authenticated"


class ForbiddenException(AppException):
    status_code = 403
    default_detail = "Forbidden"


class NotFoundException(AppException):
    status_code = 404
    default_detail = "Resource not found"


class ConflictException(AppException):
    status_code = 409
    default_detail = "Conflict"


class ServiceUnavailableException(AppException):
    status_code = 503
    default_detail = "Service unavailable"
