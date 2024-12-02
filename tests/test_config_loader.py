"""Tests the Config Loader."""

import pytest
from app.commons import ConfigLoader


@pytest.fixture
def configloader_instance() -> ConfigLoader:
    """Creates and returns an instance of the ConfigLoader pre-loaded with a set of predefined configuration settings.

    This fixture is useful for testing purposes, providing a standard configuration context to be used across
    multiple test cases. The configuration dictionary includes  details such as account information,
    data-lake storage layers, company details, and additional project-related metadata.

    :return: An instance of ConfigLoader initialized with a predefined
             configuration dictionary.
    :rtype: ConfigLoader
    """
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
    return ConfigLoader(configs)


def test_properties_for_resource_naming(configloader_instance: ConfigLoader) -> None:
    """Tests the properties for resource naming by asserting the expected company name in the `resource_name_mapping`.

    :param configloader_instance: An instance of config loader that contains
        the resource name mapping to be tested.
    :return: None
    """
    properties = configloader_instance.resource_name_mapping
    assert properties["company-name"] == "Amazon Web Services"  # noqa: S101
