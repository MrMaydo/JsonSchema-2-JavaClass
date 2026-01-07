import re
from typing import List

from src.java_model import JAVA_KEYWORDS, JAVA_BUILTIN_TYPES, JAVA_LITERALS, indent_lvl1, indent_lvl2, indent_lvl3, \
    return_indent, Field


def generate_fields_block(fields: List[Field]) -> str:
    declaration = []
    for field in fields:
        declaration.append(generate_field_declaration(field))

    return "\n".join(declaration)


def generate_field_declaration(field: Field) -> str:
    _validate_java_identifier(field.name)
    if field.description:
        javadoc = "\n".join([
            "",
            f"{indent_lvl1}/**",
            f"{indent_lvl1} * {field.description}",
            f"{indent_lvl1} */"
        ])
    else:
        javadoc = ""
    declaration = [
        javadoc,
        f"{indent_lvl1}private {field.type} {field.name};"
    ]
    return "\n".join(declaration)


def generate_getters_and_setters(fields: List[Field]) -> str:
    methods = []
    for field in fields:
        methods.append(generate_getter(field))
        methods.append(generate_setter(field))

    return "\n\n".join(methods)


def generate_getter(field: Field) -> str:
    field_name = field.name
    field_type = field.type

    _validate_java_identifier(field_name)

    getter_name = _get_getter_name(field)

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

    setter_name = _get_setter_name(field_name)

    setter = [
        "",
        f"{indent_lvl1}public void {setter_name}({field_type} {field_name}) {{",
        f"{indent_lvl2}this.{field_name} = {field_name};",
        f"{indent_lvl1}}}"
    ]
    setter = "\n".join(setter)
    return setter


def generate_equals(class_name: str, fields: List[Field]) -> str:
    equals = [
        "",
        f"{indent_lvl1}@Override",
        f"{indent_lvl1}public boolean equals(Object obj) {{",

        f"{indent_lvl2}if (this == obj)",
        f"{indent_lvl3}return true;",

        f"{indent_lvl2}if (!(obj instanceof {class_name}))",
        f"{indent_lvl3}return false;",

        f"{indent_lvl2}{class_name} that = ({class_name}) obj;"
    ]

    for i, field in enumerate(fields):
        _validate_java_identifier(field.name)
        getter_name = _get_getter_name(field)
        semicolon = ";" if i == (len(fields) - 1) else ""
        if i == 0:
            equals.append(f"{indent_lvl2}return Objects.equals({getter_name}(), that.{getter_name}()){semicolon}")
        else:
            equals.append(
                f"{indent_lvl2}{return_indent}&& Objects.equals({getter_name}(), that.{getter_name}()){semicolon}")
    equals.append(f"{indent_lvl1}}}")

    return "\n".join(equals)


def generate_hash_code(fields: List[Field]) -> str:
    hash_code = [
        "",
        f"{indent_lvl1}@Override",
        f"{indent_lvl1}public int hashCode() {{"
    ]

    for i, field in enumerate(fields):
        _validate_java_identifier(field.name)
        hash_code.extend(_get_return_hash_lines(fields, index=i))

    hash_code.append(f"{indent_lvl1}}}")

    return "\n".join(hash_code)


def _get_return_hash_lines(fields, index) -> List[str]:
    field = fields[index]
    getter_name = _get_getter_name(field)
    comma = "," if index < (len(fields) - 1) else ""
    another_hash_line = f"{indent_lvl2}{return_indent}{getter_name}(){comma}"
    if len(fields) == 1:
        return [f"{indent_lvl2}return Objects.hash({getter_name}());"]
    if len(fields) > 1 and index == 0:
        return [f"{indent_lvl2}return Objects.hash(",
                f"{another_hash_line}"]
    if len(fields) > 1 and index == (len(fields) - 1):
        return [f"{another_hash_line}",
                f"{indent_lvl2});"]
    return [another_hash_line]


def _get_getter_name(field):
    getter_name = "get" + field.name[0].upper() + field.name[1:]
    return getter_name


def _get_setter_name(field_name):
    setter_name = "set" + field_name[0].upper() + field_name[1:]
    return setter_name


def _validate_java_identifier(name: str) -> None:
    if not name:
        raise ValueError("Field name cannot be empty")

    if name in JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS:
        raise ValueError(f"'{name}' is a Java reserved keyword")

    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        raise ValueError(f"Invalid Java identifier: '{name}'")
