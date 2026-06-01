# from exceptions.handlers import AppException,NotFoundException,ConflictException,BadRequestException

__all__ = [
    "AppException",
    "NotFoundException",
    "ConflictException",
    "BadRequestException",
    "UnauthorizedException",
]


class AppException(Exception):
    """Base for all application-level errors."""

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundException(AppException):
    pass


class ConflictException(AppException):
    """Operation conflicts with existing state (e.g. duplicate email)."""


class BadRequestException(AppException):
    """Client input is invalid in a way Pydantic validation didn't catch."""


class UnauthorizedException(AppException):
    """Handled in handlers.py"""


class ForbiddenException(AppException):
    """Handled in handlers.py"""
