import re


def set_package(package: str) -> str:
    PACKAGE_REGEX = r"^(?:[a-z_][a-z0-9_]*)(?:\.(?:[a-z_][a-z0-9_]*))*$"
    if not re.match(PACKAGE_REGEX, package):
        raise ValueError(f"Invalid package: '{package}'")
    return f"package {package}"
