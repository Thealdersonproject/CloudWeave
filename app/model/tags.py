"""Tags model."""

# mypy: ignore-errors
from __future__ import annotations

from pydantic import BaseModel

from app.model import Account, Company, Project


class Tags(BaseModel):
    """This module contains the `Tags` class which represents a collection of tags.

    Tags:
    - account: An instance of the `Account` class representing the account related to the tags.
    - company: An instance of the `Company` class representing the company related to the tags.
    - project: An instance of the `Project` class representing the project related to the tags.
    - additional_tags: A dictionary of additional tags, where the keys are tag names and the values are tag values.
    This field is optional and can be `None`.

    Properties:
    - values: A dictionary containing the tags associated with the account, company, and project.
    The keys are tag names and the values are tag values. Additional tags are also included if specified.

    Methods:
    - N/A

    Usage:
    ```python
    # Create a Tags object
    tags = Tags(account=my_account, company=my_company, project=my_project, additional_tags=my_additional_tags)

    # Get the values of the tags
    tags_values = tags.Values
    ```
    """

    company: Company
    project: Project
    account: Account
    additional_tags: dict[str, str] | None

    @property
    def default(self) -> dict[str, str]:
        """Retrieves the values for the company, account, and project tags.

        Returns:
            A dictionary containing the values of the company, account, and project tags.
                 The dictionary has the following keys:
            - "Company": The name of the company.
            - "Environment": The environment of the account.
            - "Region": The region of the account.
            - "Project": The name of the project.

            Additional tags can also be added if they exist and have values in the additional_tags property.
        """
        # add company, account and project tags
        _tags: dict[str, str] = {
            "Company": self.company.name,
            "Environment": self.account.environment,
            "Region": self.account.region,
            "Project": self.project.name,
        }

        if self.additional_tags and self.additional_tags.values():
            _tags.update(self.additional_tags)

        return _tags
