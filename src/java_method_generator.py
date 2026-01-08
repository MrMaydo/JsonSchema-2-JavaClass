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
    _validate_java_field_name(field.name)

    declaration = [
        _render_javadoc(field),
        f"{indent_lvl1}private {field.type} {field.name};"
    ]
    return "\n".join(declaration)


def _render_javadoc(field: Field) -> str:
    if field.description is None:
        return ""

    return "\n".join([
        "",
        f"{indent_lvl1}/**",
        f"{indent_lvl1} * {field.description}",
        f"{indent_lvl1} */"
    ])


def generate_getters_and_setters(fields: List[Field]) -> str:
    methods = []
    for field in fields:
        methods.append(generate_getter(field))
        methods.append(generate_setter(field))

    return "\n\n".join(methods)


def generate_getter(field: Field) -> str:
    getter_name = _build_getter_name(field.name)

    getter = [
        "",
        f"{indent_lvl1}public {field.type} {getter_name}() {{",
        f"{indent_lvl2}return {field.name};",
        f"{indent_lvl1}}}"
    ]
    return "\n".join(getter)


def generate_setter(field: Field) -> str:
    setter_name = _build_setter_name(field.name)

    setter = [
        "",
        f"{indent_lvl1}public void {setter_name}({field.type} {field.name}) {{",
        f"{indent_lvl2}this.{field.name} = {field.name};",
        f"{indent_lvl1}}}"
    ]
    return "\n".join(setter)


def generate_equals(class_name: str, fields: List[Field]) -> str:
    equals = [
        "",
        f"{indent_lvl1}@Override",
        f"{indent_lvl1}public boolean equals(Object obj) {{",

        f"{indent_lvl2}if (this == obj)",
        f"{indent_lvl3}return true;",

        f"{indent_lvl2}if (!(obj instanceof {class_name}))",
        f"{indent_lvl3}return false;",

        f"{indent_lvl2}{class_name} that = ({class_name}) obj;",

        _render_equals_return_statement(fields),
        f"{indent_lvl1}}}"
    ]

    return "\n".join(equals)


def _render_equals_return_statement(fields: List[Field]) -> str:
    return_statement = []
    for i, field in enumerate(fields):
        getter_name = _build_getter_name(field.name)
        end_line = ";" if i == (len(fields) - 1) else ""
        if i == 0:
            return_statement.append(f"{indent_lvl2}return Objects.equals({getter_name}(), that.{getter_name}()){end_line}")
        else:
            return_statement.append(
                f"{indent_lvl2}{return_indent}&& Objects.equals({getter_name}(), that.{getter_name}()){end_line}")
    return "\n".join(return_statement)


def generate_hash_code(fields: List[Field]) -> str:
    hash_code = [
        "",
        f"{indent_lvl1}@Override",
        f"{indent_lvl1}public int hashCode() {{",
        _render_hashcode_return_statement(fields),
        f"{indent_lvl1}}}"
    ]

    return "\n".join(hash_code)


def _render_hashcode_return_statement(fields: List[Field]) -> str:
    if len(fields) == 1:
        return _render_hashcode_return_statement_single_field(fields)

    return _render_hashcode_return_statement_multiple_field(fields)


def _render_hashcode_return_statement_single_field(fields: List[Field]) -> str:
    field_name = fields[0].name
    getter_name = _build_getter_name(field_name)
    return f"{indent_lvl2}return Objects.hash({getter_name}());"


def _render_hashcode_return_statement_multiple_field(fields: List[Field]) -> str:
    return_statement = [f"{indent_lvl2}return Objects.hash("]
    for index, field in enumerate(fields):
        getter_name = _build_getter_name(field.name)
        comma = "," if index < (len(fields) - 1) else ""
        return_statement.append(f"{indent_lvl2}{return_indent}{getter_name}(){comma}")

    return_statement.append(f"{indent_lvl2});")

    return "\n".join(return_statement)


def _build_getter_name(field_name: str) -> str:
    _validate_java_field_name(field_name)
    return "get" + field_name[0].upper() + field_name[1:]


def _build_setter_name(field_name: str) -> str:
    _validate_java_field_name(field_name)
    return "set" + field_name[0].upper() + field_name[1:]


def _validate_java_field_name(name: str) -> None:
    if not name:
        raise ValueError("Field name cannot be empty")

    if name in JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS:
        raise ValueError(f"'{name}' is a Java reserved keyword")

    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        raise ValueError(f"Invalid Java identifier: '{name}'")
