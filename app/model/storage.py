"""Storage model."""

from __future__ import annotations

from pydantic import BaseModel


class Storage(BaseModel):
    """Represents a Storage model with different storage layers and zones.

    Attributes:
        first_layer Optional[str]: The first storage layer.
        second_layer Optional[str]: The second storage layer.
        third_layer Optional[str]: The third storage layer.
        landing_zone Optional[str]: The landing zone for the storage.
        assets Optional[str]: The assets in the storage.
    """

    first_layer: str
    second_layer: str
    third_layer: str
    landing_zone: str
    assets: str
