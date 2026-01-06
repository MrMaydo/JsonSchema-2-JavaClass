import re


def set_package(package: str) -> str:
    PACKAGE_REGEX = r"^(?:[A-Za-z_][A-Za-z0-9_]*)(?:\.(?:[A-Za-z_][A-Za-z0-9_]*))*$"
    if not re.match(PACKAGE_REGEX, package):
        raise ValueError(f"Invalid package: '{package}'")
    return f"package {package};"
