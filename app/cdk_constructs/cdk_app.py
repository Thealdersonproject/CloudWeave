"""This class is responsible to manipulate, end-to-end AWS CDK stacks."""

from aws_cdk import App


class CdkApp(App):
    """class CdkApp(App)."""

    def __init__(self) -> None:
        """Constructor for initializing the MyClass instance.

        Initializes the ProcessLogger and App components.
        """
        super().__init__()
        self._app = App()

    @property
    def app(self) -> App:
        """Property to return App.

        :return: The application instance.
        """
        return self._app
