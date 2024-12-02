"""CloudWeave Models Module.

This module defines the core data models and entities used throughout the CloudWeave framework.
These models provide standardized representations of infrastructure components, organizational
structures, and resource metadata across different cloud providers.

Models:
    - Account: Represents cloud provider accounts and their associated credentials/configurations
    - Company: Defines organizational structure and company-wide settings
    - Project: Encapsulates project-specific configurations and resource groupings
    - Storage: Represents storage resource configurations across different providers
    - Tags: Standardizes resource tagging and metadata management

These models serve as the foundation for CloudWeave's abstraction layer, ensuring
consistent data structures and relationships regardless of the underlying cloud provider.

Example:
    from app.models import Project, Tags

    project = Project(
        name="data-pipeline",
        environment="production",
        tags=Tags(
            owner="data-team",
            cost_center="analytics"
        )
    )

Key Features:
    - Provider-agnostic data structures
    - Standardized validation and type checking
    - Consistent interface across different cloud implementations
    - Built-in serialization for configuration management

Note:
    All models implement proper data validation and follow CloudWeave's
    standardization principles to ensure compatibility across different
    cloud provider implementations.

See Also:
    - CloudWeave Configuration Guide
    - Resource Naming Conventions
"""

from .account import Account
from .company import Company
from .project import Project
from .storage import Storage
from .tags import Tags

__all__ = ["Account", "Company", "Project", "Storage", "Tags"]
