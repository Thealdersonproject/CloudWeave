"""AWS KMS key implementation."""

from dataclasses import dataclass
from typing import Any

from aws_cdk import aws_kms as kms
from cloudweave.core import Environment
from constructs import Construct


@dataclass
class KMSKeyConfig:
    """Configuration for KMS key creation or lookup for existing key."""

    alias: str
    description: str
    project: str
    environment: Environment
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
        self.key_name = self._create_key_name()
        self.alias_name = f"alias/{self.key_name}"

        # Create or use existing key
        self.key = self._create_or_use_key()

    def _create_key_name(self) -> str:
        """Create standardized key name."""
        parts: list[Any] = [self.config.project, self.config.alias, self.config.environment.value]
        return "-".join(parts)

    def _create_or_use_key(self) -> kms.IKey | kms.Key:
        """Create new key or use existing one by alias."""
        try:
            # Try to look up existing key by alias
            return kms.Alias.from_alias_name(self.scope, f"{self.key_name}-lookup", self.alias_name).target_key
        except:
            # Key doesn't exist, create new one
            return self._create_new_key()

    def _create_new_key(self) -> kms.Key:
        """Create new KMS key."""
        key = kms.Key(
            self.scope,
            self.key_name,
            alias=self.alias_name,
            description=self.config.description,
            enable_key_rotation=self.config.enable_key_rotation,
            removal_policy=self.config.removal_policy,
            enabled=True,
        )

        # Add administrators if specified
        if self.config.administrators:
            for admin in self.config.administrators:
                key.grant_admin(admin)

        # Add users if specified
        if self.config.users:
            for user in self.config.users:
                key.grant_encrypt_decrypt(user)

        # Add tags
        self._add_tags(key)

        return key

    def _add_tags(self, key: kms.Key) -> None:
        """Add standard tags to the key."""
        tags = {
            "Project": self.config.project,
            "Environment": self.config.environment.value,
            "Owner": self.config.owner,
            "ManagedBy": "cloudweave",
        }

        if self.config.cost_center:
            tags["CostCenter"] = self.config.cost_center
        if self.config.team:
            tags["Team"] = self.config.team

        for key_name, value in tags.items():
            key.add_to_resource_policy(key_name, value)

    @property
    def key_arn(self) -> str:
        """Get the key ARN."""
        return self.key.key_arn

    @property
    def key_id(self) -> str:
        """Get the key ID."""
        return self.key.key_id
