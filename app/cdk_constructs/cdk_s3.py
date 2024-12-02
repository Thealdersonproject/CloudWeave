"""This class is responsible to manipulate, end-to-end S3 buckets within AWS CDK stacks."""

from typing import Any, ParamSpec

from aws_cdk import Stack, Tags, aws_s3 as s3
from constructs import Construct
from loguru import logger

from app.commons import constants, resource_name_pattern as name_utils

P = ParamSpec("P")


class CdkS3(Stack):
    """S3 class provides utilities for managing AWS S3 buckets within AWS CDK stacks.

    useful links:
        Reference aws_cdk.aws_s3 - Bucket: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        Naming rules: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs: P.kwargs) -> None:  # type: ignore[valid-type]
        """Initializes Cdk S3 class.

        :param scope: The scope in which this construct is defined.
        :type scope: Construct
        :param construct_id: Unique identifier for this construct.
        :type construct_id: str
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        """
        super().__init__(scope, construct_id, **kwargs)
        self.scope = scope
        self.resource_name_pattern: str | None = None

    @staticmethod
    def _format_bucket_name(logical_name: str) -> str:
        """Sets the resource name in the expected pattern to be used for the S3 bucket as per AWS standards.

        :param logical_name: Logical name provided by the user, which will be used to generate the resource
        name pattern. It must be a non-empty string.
        :return: None
        """
        if not logical_name:
            msg = "Logical name must be provided."
            raise ValueError(msg)

        resource_name: str = name_utils.format_name(
            allow_upper_case=False,
            forbidden_chars=["_", "."],
            forbidden_start=["xn--", "sthree-", "sthree-configurator", "amzn-s3-demo-"],
            forbidden_end=["-s3alias", "--ol-s3", ".mrap", "--x-s3"],
            name=logical_name,
            name_separator=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
            forbidden_chars_new_value=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
        )

        logger.info("Bucket name defined as: {}", resource_name)
        return resource_name

    def create_bucket(  # type: ignore[valid-type]
        self,
        bucket_name: str,
        bucket_id: str | None,
        tags: dict[str, str],
        **kwargs: Any,  # noqa: ANN401
    ) -> s3.Bucket:
        """Creates an S3 bucket with the specified parameters and returns the bucket object.

        Arguments:
            bucket_id (Optional[str]): The ID of the bucket. If not provided, the bucket_name will be used as the ID.
            bucket_name (str): The name of the S3 bucket. Must not be empty or blank.
            tags (dict[str, str]): A dictionary of tags to add to the S3 bucket.
            **kwargs: Additional keyword arguments that are passed to the S3 bucket constructor.

        Returns:
            cdk.aws_s3.Bucket: The created S3 bucket object.

        Raises:
            ValueError: If the bucket_name is empty or blank.
        """
        if not bucket_name or bucket_name.strip():
            msg = "Bucket name cannot be empty"
            raise ValueError(msg)

        if not bucket_id or bucket_id.strip():
            bucket_id = bucket_name

        # sets the bucket name as per given parameter.
        bucket_name = CdkS3._format_bucket_name(bucket_name)

        bucket = s3.Bucket(
            scope=self.scope,
            id=bucket_id,
            bucket_name=bucket_name,
            enforce_ssl=True,
            minimum_tls_version=1.2,
            **kwargs,
        )
        logger.info("Bucket {} object created.", bucket.bucket_name)

        # S3 default tags
        Tags.of(bucket).add(key="resource", value="s3 bucket")

        # Add tags to the S3 bucket
        for key in tags:
            Tags.of(bucket).add(key=key, value=tags[key])
            logger.info("Tag {} = {} added to Bucket {}", key, tags[key], bucket.bucket_name)

        return bucket
