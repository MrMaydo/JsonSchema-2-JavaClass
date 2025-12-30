import re
from dataclasses import dataclass
from typing import List


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


def generate_getters_and_setters(fields: List[Field]) -> str:
    methods: list[str] = []
    for field in fields:
        methods.append(generate_getter(field))
        methods.append(generate_setter(field))

    return "\n\n".join(methods)


def generate_getter(field: Field) -> str:
    field_name = field.name
    field_type = field.type

    _validate_java_identifier(field_name)

    getter_name = "get" + field_name[0].upper() + field_name[1:]

    getter = [
        "",
        f"{indent_lvl1}public {field_type} {getter_name}() {{",
        f"{indent_lvl2}return {field_name};",
        f"{indent_lvl1}}}"
    ]
    getter = "\n".join(getter)

    return getter


def generate_setter(field: Field) -> str:
    field_name = field.name
    field_type = field.type

    _validate_java_identifier(field_name)

    setter_name = "set" + field_name[0].upper() + field_name[1:]

    setter = [
        "",
        f"{indent_lvl1}public void {setter_name}({field_type} {field_name}) {{",
        f"{indent_lvl2}this.{field_name} = {field_name};",
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

