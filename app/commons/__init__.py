"""CloudWeave Commons Module.

This module provides core utilities and shared functionality used throughout the CloudWeave framework.
It includes essential tools for configuration management, resource naming, environment handling,
and design pattern implementations.

Components:
    - ConfigLoader: Manages configuration loading and parsing across different environments
    - format_name: Standardizes resource naming patterns across cloud providers
    - get_env: Retrieves and validates environment variables
    - singleton: Decorator for implementing the singleton pattern

These utilities form the foundation for CloudWeave's cloud abstraction layer,
ensuring consistent behavior and patterns across different cloud implementations.

Example:
    from app.commons import ConfigLoader, get_env

    config = ConfigLoader()
    current_env = get_env('ENVIRONMENT')

Note:
    All components in this module are designed to be cloud-provider agnostic
    and follow CloudWeave's principle of unified abstraction.
"""

from .common_decorators import singleton
from .config_loader import ConfigLoader
from .resource_name_pattern import format_name
from .utils import get_env

__all__ = ["ConfigLoader", "format_name", "get_env", "singleton"]
