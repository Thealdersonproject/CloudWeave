"""Project model."""

from __future__ import annotations

from pydantic import BaseModel


class Project(BaseModel):
    """This is the documentation for the `Project` class.

    Attributes:
        name (str): The name of the project.
        short_name (str): The short name of the project.

    """

    name: str
    short_name: str
