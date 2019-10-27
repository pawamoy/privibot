"""
privibot package.

A library to build Telegram Bot with a privilege system.

If you read this message, you probably want to learn about the library and not the command-line tool:
please refer to the README.md included in this package to get the link to the official documentation.
"""

from . import callbacks
from .database import User, UserPrivilege, init
from .decorators import require_access, require_admin, require_privileges
from .privileges import Privilege, Privileges

__all__ = [
    "callbacks",
    "User",
    "UserPrivilege",
    "init",
    "require_privileges",
    "require_admin",
    "require_access",
    "Privileges",
    "Privilege",
]
