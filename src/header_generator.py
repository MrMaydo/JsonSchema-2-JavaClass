import re
from typing import List, Union

from src.java_model import Field, indent


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


def render_javadoc(description: Union[str, None], indent_lvl: int) -> str:
    if not description:
        return ""

    return "\n".join([
        "",
        f"{indent(indent_lvl)}/**",
        f"{indent(indent_lvl)} * {description}",
        f"{indent(indent_lvl)} */"
    ])


_imports = {
    "Date": "import java.util.Date;",
    "List": "import java.util.List;",
    "Objects": "import java.util.Objects;",
}
