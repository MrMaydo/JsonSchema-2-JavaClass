import re
from dataclasses import dataclass


JAVA_KEYWORDS = {
    "abstract", "assert", "boolean", "break", "byte", "case", "catch",
    "char", "class", "const", "continue", "default", "do", "double",
    "else", "enum", "extends", "final", "finally", "float", "for",
    "goto", "if", "implements", "import", "instanceof", "int",
    "interface", "long", "native", "new", "package", "private",
    "protected", "public", "return", "short", "static", "strictfp",
    "super", "switch", "synchronized", "this", "throw", "throws",
    "transient", "try", "void", "volatile", "while"
}

JAVA_BUILTIN_TYPES = {
    "Boolean", "Byte", "Character", "Double", "Float", "Integer", "List", "Long", "Short",
    "Class", "Object", "String", "Void"
}

JAVA_LITERALS = {
    "null", "true", "false"
}

indent_lvl1 = "    "
indent_lvl2 = indent_lvl1 * 2
indent_lvl3 = indent_lvl1 * 3


@dataclass
class Field:
    name: str
    type: str


def generate_getter(attr: Field) -> str:
    attr_name = attr.name
    attr_type = attr.type

    _validate_java_identifier(attr_name)

    getter_name = "get" + attr_name[0].upper() + attr_name[1:]

    getter = [
        "",
        f"{indent_lvl1}public {attr_type} {getter_name}() {{",
        f"{indent_lvl2}return {attr_name};",
        f"{indent_lvl1}}}"
    ]
    getter = "\n".join(getter)

    return getter


def generate_setter(attr: Field) -> str:
    attr_name = attr.name
    attr_type = attr.type

    _validate_java_identifier(attr_name)

    setter_name = "set" + attr_name[0].upper() + attr_name[1:]

    setter = [
        "",
        f"{indent_lvl1}public void {setter_name}({attr_type} {attr_name}) {{",
        f"{indent_lvl2}this.{attr_name} = {attr_name};",
        f"{indent_lvl1}}}"
    ]
    setter = "\n".join(setter)
    return setter


def _validate_java_identifier(name: str) -> None:
    if not name:
        raise ValueError("Field name cannot be empty")

    if name in JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS:
        raise ValueError(f"'{name}' is a Java reserved keyword")

    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        raise ValueError(f"Invalid Java identifier: '{name}'")

