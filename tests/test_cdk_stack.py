"""Tests the Config Loader."""

import aws_cdk as core
from app.cdk_constructs import CdkStack
from app.commons import ConfigLoader
from aws_cdk import assertions
from loguru import logger


def test_properties_for_resource_naming() -> None:
    """Docstring for this test."""
    configs = {
        "account": {
            "id": "ACCOUNT_ID",
            "region": "REGION_ID",
            "environment": "ENVIRONMENT_NAME",
        },
        "data-lake-storage": {
            "first_layer": "raw",
            "second_layer": "stage",
            "third_layer": "analytics",
            "landing_zone": "landing",
            "assets": "data-lake-assets",
        },
        "company": {"name": "Amazon Web Services", "short_name": "aws"},
        "project": {"name": "Data Lakehouse", "short_name": "dlh"},
        "additional-tags": {"tag": "Me"},
    }
    core.App()

    ConfigLoader(configs)
    stack = CdkStack(app=None, stack_id="My Stack", description="This is my test sTaCk").stack
    assertions.MatchResult(stack)
    assertions.Template.from_stack(
        stack=stack,
    )
    logger.info("Stack name: {}", stack.stack_name)
    logger.info("Environment: {}", stack.environment)
    logger.info("Region: {}", stack.region)

    assert stack.stack_name == "my-stack"  # noqa: S101
