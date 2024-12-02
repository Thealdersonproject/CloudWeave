"""This class is for all and any encryption keys and services."""

from loguru import logger

from app.commons import ConfigLoader


class Encryption:
    """Class to handle encryption for resources."""

    _AWS_KMS_KEY_SHORT_NAME = "kms"

    def __init__(self) -> None:
        """Initializes Encryption class."""
        company_name = ConfigLoader().company.name
        logger.info("Hello World", company_name)
