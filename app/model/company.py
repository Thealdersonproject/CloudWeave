"""Company model."""

# mypy: ignore-errors
from __future__ import annotations

from pydantic import BaseModel


class Company(BaseModel):
    """Company class inherits from BaseModel and represents a company entity.

    Attributes:
        name (str): The full name of the company.
        short_name (str): The short name or abbreviation of the company.
    """

    name: str
    short_name: str
