"""Creates naming pattern for resources."""

import re


def format_name(
    name: str,
    name_separator: str,
    forbidden_chars: list[str],
    forbidden_start: list[str],
    forbidden_end: list[str],
    forbidden_chars_new_value: str,
    *,
    allow_upper_case: bool,
) -> str:
    """Formats the name of the resource as per pattern.

    :param name: The initial name to format.
    :param name_separator: The character used to separate words in the resource name.
    :param forbidden_chars: List of characters that are not allowed in the resource name.
    :param forbidden_start: List of characters that the resource name should not start with.
    :param forbidden_end: List of characters that the resource name should not end with.
    :param forbidden_chars_new_value:
        The character that will replace forbidden characters in the resource name.
    :param allow_upper_case:
        Flag indicating whether uppercase characters are allowed in the resource name.
    :return: The formatted resource name.
    """
    name = name.strip().lower() if not allow_upper_case else name.strip()

    for clean_name in forbidden_chars:
        name = name.replace(clean_name, f"{forbidden_chars_new_value}")

    clean_resource_name_completed: bool = False
    while not clean_resource_name_completed:
        clean_resource_name_completed = True
        for clean_start in forbidden_start:
            if name.startswith(clean_start.strip()):
                name = name[len(clean_start) :]
                clean_resource_name_completed = False

    clean_resource_name_completed = False
    while not clean_resource_name_completed:
        clean_resource_name_completed = True
        for clean_end in forbidden_end:
            if name.endswith(clean_end.strip()):
                name = name[: len(clean_end)]
                clean_resource_name_completed = False

    name = re.sub(rf"{name_separator}+", f"{name_separator}", name)
    name = re.sub(r"\s+", " ", name)

    return name.replace(" ", f"{name_separator}")
