from .client import AuthClient, UsersClient, _Http
from .exceptions import (
    APIError,
    AuthError,
    FlexslolError,
    NotAuthenticatedError,
    UserNotFoundError,
)
from .models import CustomBadge, Session, User


class Client:
    """
    Entry point for the flexs.lol mommy api.

    Attributes
    ----------
    auth  : AuthClient   — signup / login / logout / refresh
    users : UsersClient  — list / get / search / update users
    """

    def __init__(self) -> None:
        _http = _Http()
        self.auth = AuthClient(_http)
        self.users = UsersClient(_http)

    def __repr__(self) -> str:
        state = "authenticated" if self.auth.is_authenticated else "unauthenticated"
        return f"<flexslol.Client [{state}]>"


__all__ = [
    "Client",
    "User",
    "Session",
    "CustomBadge",
    "FlexslolError",
    "AuthError",
    "NotAuthenticatedError",
    "UserNotFoundError",
    "APIError",
]

__version__ = "1.0.0"
