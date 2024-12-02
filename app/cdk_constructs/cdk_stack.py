"""This class is responsible to manipulate, end-to-end AWS CDK stacks."""

from aws_cdk import App, Environment, Stack
from loguru import logger

from app.cdk_constructs.cdk_app import CdkApp
from app.commons import ConfigLoader, constants, resource_name_pattern as name_utils


class CdkStack(Stack):
    """Initializes the Object with application, configuration loader, logger, and environment.

    :param app: Optional application parameter which can be of type App or None.
    """

    def __init__(
        self, *, app: App | None, stack_id: str, description: str | None, tags: dict[str, str] | None = None
    ) -> None:
        """Initializes the Object with application, configuration loader, logger, and environment.

        :param app: Optional application parameter which can be of type App or None.
        :param stack_id: The unique identifier for the stack, must be a non-empty string.
        :param description: A description for the stack. If None, the stack_id will be used.
        :param tags: A dictionary of key-value pairs for tagging the stack, optional.
        :return: A newly created Stack object.

        :raises ValueError: If the stack_id is not a non-empty string.
        """
        super().__init__()
        app = app if app else CdkApp().app

        env = Environment(
            account=ConfigLoader().account.id,  # type: ignore[union-attr]
            region=ConfigLoader().account.region,  # type: ignore[union-attr]
        )
        logger.debug("Environment account: {} / region: {}", env.account, env.region)

        if not stack_id or not stack_id.strip():
            msg = "Stack id must be a non-empty string."
            raise ValueError(msg)

        stack_id = name_utils.format_name(
            name=stack_id,
            name_separator=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
            allow_upper_case=False,
            forbidden_chars=[],
            forbidden_start=[],
            forbidden_end=[],
            forbidden_chars_new_value=constants.HYPHEN_RESOURCE_NAME_PATTERN_SEPARATOR,
        )
        description = description if description else stack_id

        self._stack = Stack(
            scope=app,
            id=stack_id,
            description=description,
            tags=tags,
            env=env,
        )

    @property
    def stack(self) -> Stack:
        """Returns the stack object."""
        return self._stack
