"""Loads information to be used in different modules."""

import sys

from loguru import logger

from app.commons import singleton, utils
from app.model import Account, Company, Project, Storage, Tags


@singleton
class ConfigLoader:
    """ConfigLoader is a singleton class responsible for loading and managing configuration settings.

    Attributes:
        logger (loguru.logger): Singleton logger instance for logging.
        _company (Company): Loaded company information.
        _account (Account): Loaded account information.
        _project (Project): Loaded project information.
        _tags (Tags): Loaded tags information.
        _storage (Storage): Loaded storage information.
        _properties_for_resource_name_mapping (dict[str, str]): Dictionary for resource name mapping properties.
    """

    def __init__(self, configs: dict[str, dict[str, str]] | None) -> None:
        """Initializes the ConfigLoader object.

        :param configs: A dictionary containing configuration settings required for initializing the ProcessLogger
        and loading various information such as company, project, account, storage, and additional tags.
        The keys should include 'company', 'project', 'account', 'data-lake-storage', and 'additional-tags'.
        """
        logger.remove()
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>\
            {function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
        )
        self.logger = logger
        # loads basic information for resource naming
        self._company: Company = self._load_company_information(configs=configs.get("company", {}))  # type: ignore[union-attr]
        self._account: Account = self._load_account_information(configs=configs.get("account", {}))  # type: ignore[union-attr]
        self._project: Project = self._load_project_information(configs=configs.get("project", {}))  # type: ignore[union-attr]
        self._tags: Tags = self._load_tags(additional_tags=configs.get("additional-tags", {}))  # type: ignore[union-attr]
        self._storage: Storage = self._load_storage_information(configs=configs.get("data-lake-storage", {}))  # type: ignore[union-attr]

        # loads the models information for name mapping
        self._properties_for_resource_name_mapping: dict[str, str] = self._load_properties_for_resource_naming()

    @property
    def company(self) -> Company:
        """Returns the company associated with the current instance.

        :return: Company instance.
        """
        return self._company

    @property
    def account(self) -> Account:
        """Returns the account associated with the current instance.

        :return: Account instance.
        """
        return self._account

    @property
    def project(self) -> Project:
        """Returns the project associated with the current instance.

        :return: The project instance.
        """
        return self._project

    @property
    def tags(self) -> Tags:
        """Gets the tags associated with this entity.

        :return: Tags related to the entity.
        :rtype: Tags
        """
        return self._tags

    @property
    def storage(self) -> Storage:
        """Returns the current instance of the storage.

        :return: The storage instance associated with this object.
        """
        return self._storage

    @property
    def resource_name_mapping(self) -> dict[str, str] | None:
        """Property for resource name mapping.

        :return: Dictionary that provides a mapping of resource names to their respective properties
        """
        return self._properties_for_resource_name_mapping

    def _load_company_information(self, *, configs: dict[str, str]) -> Company:
        """Loads company information based on the provided configuration.

        :param configs: A dictionary containing configuration parameters for company initialization.
        :type configs: dict[str, str]
        :return: An instance of the Company class initialized with the provided configurations.
        :rtype: Company
        """
        company = Company(**configs)
        self.logger.info(  # noqa: PLE1205
            "Company: name {}, short-name {}.",
            company.name,
            company.short_name,
        )

        return company

    def _load_project_information(self, *, configs: dict[str, str]) -> Project:
        """Loads project information and initializes a Project instance.

        :param configs: A dictionary containing project configuration details with keys as configuration
            names and values as configuration settings.
        :type configs: dict[str, str]
        :return: An instance of Project initialized with the provided configurations.
        :rtype: Project
        """
        project = Project(**configs)
        self.logger.info(  # noqa: PLE1205
            "Project: name {}, short-name {}.",
            project.name,
            project.short_name,
        )

        return project

    def _load_account_information(self, *, configs: dict[str, str]) -> Account:
        """Loads company information.

        :param configs: Dictionary containing configuration keys for account information.
        :type configs: dict[str, str]
        :return: Account object populated with id, region, and environment information.
        :rtype: Account
        """
        account_id_key: str = configs["id"]
        account_id: str = utils.get_env(key=account_id_key)

        account_region_key: str = configs["region"]
        account_region: str = utils.get_env(key=account_region_key)

        account_environment_key: str = configs["environment"]
        account_environment: str = utils.get_env(key=account_environment_key)

        account = Account(id=account_id, region=account_region, environment=account_environment)
        self.logger.info(  # noqa: PLE1205
            "Account: id {}, region {}, environment {}.",
            account.id,
            account.region,
            account.environment,
        )

        return account

    def _load_storage_information(self, *, configs: dict[str, str]) -> Storage:
        """Loads storage information based on the provided configuration dictionary.

        :param configs: A dictionary containing storage configuration.
        :type configs: dict[str, str]
        :return: An initialized Storage object based on provided configurations.
        :rtype: Storage
        """
        storage = Storage(**configs)
        self.logger.info("Storage Information")
        self.logger.info(" :: First layer :: >> {}.", storage.first_layer)  # noqa: PLE1205
        self.logger.info(" :: Second layer :: >> {}.", storage.second_layer)  # noqa: PLE1205
        self.logger.info(" :: Third layer :: >> {}.", storage.third_layer)  # noqa: PLE1205
        self.logger.info(" :: Landing-zone :: >> {}.", storage.landing_zone)  # noqa: PLE1205
        self.logger.info(" :: Assets folder :: >> {}.", storage.assets)  # noqa: PLE1205

        return storage

    def _load_tags(self, *, additional_tags: dict[str, str] | None) -> Tags:
        """Loads tags information.

        :param additional_tags: Dictionary containing additional tags to be loaded.
        :return: None
        """
        tags = Tags(
            company=self.company,
            project=self.project,
            account=self.account,
            additional_tags=additional_tags,
        )

        self.logger.info("Tags Information")
        for tag, value in tags.default.items():
            self.logger.info("::{}:: >> {}", tag, value)  # noqa: PLE1205

        return tags

    def _load_properties_for_resource_naming(self) -> dict[str, str]:
        """Populates the properties_for_resource_naming attribute with company, project, and account-related data.

        :return: None
        """
        _properties_for_resource_name_mapping = {
            "company-name": self.company.name,  # type: ignore[union-attr]
            "company-short_name": self.company.short_name,  # type: ignore[union-attr]
            "project-name": self.project.name,  # type: ignore[union-attr]
            "project-short_name": self.project.short_name,  # type: ignore[union-attr]
            "account-id": self.account.id,  # type: ignore[union-attr]
            "account-region": self.account.region,  # type: ignore[union-attr]
            "account-environment": self.account.environment,  # type: ignore[union-attr]
        }
        self.logger.info("Properties for resource naming:")
        for key, value in _properties_for_resource_name_mapping.items():
            self.logger.info("::{}:: >> {}", key, value)  # noqa: PLE1205

        return _properties_for_resource_name_mapping
