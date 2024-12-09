"""Core type definitions for CloudWeave."""

from dataclasses import dataclass
from enum import Enum


class Provider(str, Enum):
    """Supported cloud providers."""

    AWS = "aws"


class Environment(str, Enum):
    """Supported environments."""

    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


@dataclass(frozen=True)
class BaseConfig:
    """Base configuration for all resources."""

    project: str
    environment: Environment
    owner: str
    cost_center: str | None = None
    team: str | None = None
