import re
from typing import List

from java_model import Field


def set_package(package: str) -> str:
    PACKAGE_REGEX = r"^(?:[A-Za-z_][A-Za-z0-9_]*)(?:\.(?:[A-Za-z_][A-Za-z0-9_]*))*$"
    if not re.match(PACKAGE_REGEX, package):
        raise ValueError(f"Invalid package: '{package}'")
    return f"package {package};"


def set_imports(fields: List[Field]) -> str:
    imports = [_imports["Objects"]]
    for field in fields:
        if field.type in _imports.keys():
            imports.append(_imports[field.type])
    imports.sort()
    return "\n".join(imports)


_imports = {
    "Date": "import java.util.Date;",
    "List": "import java.util.List;",
    "Objects": "import java.util.Objects;",
}
