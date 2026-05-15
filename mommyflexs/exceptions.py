class FlexslolError(Exception):
    """Base exception for all flexslol errors."""


class AuthError(FlexslolError):
    """Raised when authentication fails (login / signup)."""


class NotAuthenticatedError(FlexslolError):
    """Raised when a method that requires a session is called without one."""


class UserNotFoundError(FlexslolError):
    """Raised when a requested user does not exist."""


class APIError(FlexslolError):
    """Raised when the API returns an unexpected status code."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}")
