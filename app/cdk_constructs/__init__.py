"""CloudWeave AWS CDK Constructors Module.

This module provides a collection of high-level AWS CDK constructs that implement
CloudWeave's abstraction patterns for AWS infrastructure. It encapsulates common AWS
resources and patterns while maintaining CloudWeave's standardized interface.

Components:
    - CdkApp: Base application construct for AWS CDK applications
    - CdkKms: Abstracted KMS key management and encryption patterns
    - CdkS3: Enhanced S3 bucket constructs with standardized configurations
    - CdkStack: Base stack construct with CloudWeave's common patterns

These constructors implement CloudWeave's infrastructure patterns specifically for AWS,
while maintaining consistency with other cloud provider implementations.

Example:
    from app.aws.constructors import CdkApp, CdkStack

    app = CdkApp()
    stack = CdkStack(app, "MyStack")

    # Add resources to the stack
    bucket = CdkS3(stack, "DataBucket")

Note:
    All constructors follow CloudWeave's naming conventions and security best practices,
    while providing seamless integration with AWS CDK's native capabilities.

See Also:
    - AWS CDK Documentation: https://docs.aws.amazon.com/cdk/
    - CloudWeave Common Patterns Documentation
"""

from .cdk_app import CdkApp
from .cdk_kms import CdkKms
from .cdk_s3 import CdkS3
from .cdk_stack import CdkStack

__all__ = ["CdkApp", "CdkKms", "CdkS3", "CdkStack"]
