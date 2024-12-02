"""This class is responsible to manipulate, end-to-end S3 buckets within AWS CDK stacks."""

from typing import ParamSpec

from aws_cdk import Stack, aws_kms as kms
from constructs import Construct

P = ParamSpec("P")


class CdkKms(Stack):
    """Kms class provides utilities for managing AWS KMS keys.

    useful links:
        Reference aws_cdk.aws_kms - KMS: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_kms/Key.html
        Naming rules: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
    """

    @staticmethod
    def create_kms_key(scope: Construct, key_name: str, **kwargs: P.kwargs) -> kms.Key:  # type: ignore[valid-type]
        """Creates a KMS key.

        :param scope:
        :param key_name: Name to be used for the key and also for the alias.
        :param kwargs: Additional keyword arguments.
        :return: kms.Key: AWS KMS key.
        """
        kms_key: kms.Key = kms.Key(scope=scope, id=key_name, **kwargs)
        return kms_key
