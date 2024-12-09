"""AWS KMS key implementation."""

from dataclasses import dataclass

from aws_cdk import aws_kms as kms
from constructs import Construct

from cloudweave.core.naming import (
    AWSResourceType,
    AWSTagConfig,
    create_aws_resource_name,
)


@dataclass
class KMSKeyConfig:
    """Configuration for KMS key creation."""

    alias: str
    description: str
    project: str
    environment: str
    owner: str
    enable_key_rotation: bool = True
    removal_policy: str = "RETAIN"
    administrators: list[str] | None = None
    users: list[str] | None = None
    cost_center: str | None = None
    team: str | None = None


class KMSKey:
    """AWS KMS key resource."""

    def __init__(
        self,
        scope: Construct,
        config: KMSKeyConfig,
    ) -> None:
        """Initialize KMS key resource.

        Args:
            scope: CDK construct scope
            config: KMS key configuration
        """
        self.scope = scope
        self.config = config

        # Create key name and alias
        self.key_name: str = create_aws_resource_name(
            project=config.project,
            resource=config.alias,
            environment=config.environment,
            resource_type=AWSResourceType.KMS_KEY,  # pyright: ignore [reportUnknownMemberType]
        )

        self.alias_name = f"alias/{self.key_name}"

        # Create tags
        self.tags = AWSTagConfig(
            project=config.project,
            environment=config.environment,
            owner=config.owner,
            cost_center=config.cost_center,
            team=config.team,
        )

        # Create or use existing key
        self.key = self._create_or_use_key()

    def _create_or_use_key(self) -> kms.IKey | kms.Key:
        """Create new key or use existing one by alias."""
        try:
            # Try to look up existing key by alias
            return kms.Alias.from_alias_name(self.scope, f"{self.key_name}-lookup", self.alias_name).target_key
        except:  # noqa: E722
            # Key doesn't exist, create new one
            return kms.Key(
                self.scope,
                self.key_name,
                alias=self.alias_name,
                description=self.config.description,
                enable_key_rotation=self.config.enable_key_rotation,
                removal_policy=self.config.removal_policy,
                admins=self.config.administrators,
                enabled=True,
            )

    @property
    def key_arn(self) -> str:
        """Get the key ARN."""
        return self.key.key_arn

    @property
    def key_id(self) -> str:
        """Get the key ID."""
        return self.key.key_id
