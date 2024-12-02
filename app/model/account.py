"""Account model."""

# mypy: ignore-errors
from __future__ import annotations

from pydantic import BaseModel


class Account(BaseModel):
    """The Account class represents an account in the system. It is a subclass of the BaseModel class.

    Attributes:
        id (str): The unique identifier of the account.
        region (str): The region where the account is located.
        environment (str): The environment in which the account is running.

    """

    id: str
    region: str
    environment: str
