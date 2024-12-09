"""Resource naming patterns and conventions."""

from dataclasses import dataclass
from enum import Enum

from .types import Environment


class AWSResourceType(str, Enum):
    """AWS Resource types with their naming patterns."""

    KMS_KEY = "kms-key"
    SECRET = "secret"
    S3_BUCKET = "s3-bucket"
    IAM_ROLE = "iam-role"
    LOG_GROUP = "log-group"


class Separator(str, Enum):
    """Name separators for different resource types."""

    HYPHEN = "-"  # Most AWS resources (KMS, IAM, S3)
    SLASH = "/"  # Secrets, Log Groups
    UNDERSCORE = "_"  # Databases
    DOT = "."  # Certificates


@dataclass(frozen=True)
class ResourceName:
    """Resource name handler."""

    project: str
    resource: str
    environment: Environment
    extra_parts: list[str] | None = None

    def with_separator(self, separator: Separator) -> str:
        """Get formatted resource name with specified separator.

        Args:
            separator: Separator to use between name parts

        Returns:
            Formatted resource name
        """
        parts = [self.project, self.resource, self.environment.value]

        if self.extra_parts:
            parts.extend(self.extra_parts)

        return separator.join(parts)


@dataclass(frozen=True)
class AWSName(ResourceName):
    """AWS-specific resource name handler."""

    # Move non-default argument before the inherited default argument
    resource_type: AWSResourceType | None = None
    extra_parts: list[str] | None = None

    def __post_init__(self) -> None:
        """Initialize with resource type specific separator."""
        super().__post_init__()
        # Using object.__setattr__ because dataclass is frozen
        object.__setattr__(
            self,
            "_separator_map",
            {
                AWSResourceType.KMS_KEY: Separator.HYPHEN,
                AWSResourceType.SECRET: Separator.SLASH,
                AWSResourceType.S3_BUCKET: Separator.HYPHEN,
                AWSResourceType.IAM_ROLE: Separator.HYPHEN,
                AWSResourceType.LOG_GROUP: Separator.SLASH,
            },
        )


@dataclass(frozen=True)
class TagConfig:
    """Resource tagging configuration."""

    project: str
    environment: Environment
    owner: str
    cost_center: str | None = None
    team: str | None = None

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary of tags.

        Returns:
            Dictionary of tags
        """
        tags = {
            "Project": self.project,
            "Environment": self.environment.value,
            "Owner": self.owner,
            "ManagedBy": "cloudweave",
        }

        if self.cost_center:
            tags["CostCenter"] = self.cost_center
        if self.team:
            tags["Team"] = self.team

        return tags


def create_aws_resource_name(
    project: str,
    resource: str,
    environment: Environment,
    resource_type: AWSResourceType,
    extra_parts: list[str] | None = None,
) -> str:
    """Create standardized AWS resource name.

    Args:
        project: Project identifier
        resource: Resource identifier
        environment: Environment (dev, staging, prod)
        resource_type: Type of AWS resource
        extra_parts: Optional additional name parts

    Returns:
        Formatted resource name according to AWS resource type
    """
    name = AWSName(
        project=project,
        resource=resource,
        environment=environment,
        resource_type=resource_type,
        extra_parts=extra_parts,
    )
    return name.get_name()
