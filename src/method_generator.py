import re
from dataclasses import dataclass
from typing import List, Optional

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
    description: Optional[str] = None


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
        getter_name = "get" + field.name[0].upper() + field.name[1:]
        semicolon = ";" if i == (len(fields) - 1) else ""
        if i == 0:
            equals.append(f"{indent_lvl2}return Objects.equals({getter_name}(), that.{getter_name}()){semicolon}")
        else:
            equals.append(f"{indent_lvl2}        && Objects.equals({getter_name}(), that.{getter_name}()){semicolon}")
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
        getter_name = "get" + field.name[0].upper() + field.name[1:]
        comma = "," if i < (len(fields) - 1) else ""

        if len(fields) == 1:
            hash_code.append(f"{indent_lvl2}return Objects.hash({getter_name}());")
        elif len(fields) > 1 and i == 0:
            hash_code.append(f"{indent_lvl2}return Objects.hash(")
            hash_code.append(f"{indent_lvl2}        {getter_name}(){comma}")
        elif len(fields) > 1 and i == (len(fields) - 1):
            hash_code.append(f"{indent_lvl2}        {getter_name}(){comma}")
            hash_code.append(f"{indent_lvl2});")
        else:
            hash_code.append(f"{indent_lvl2}        {getter_name}(){comma}")

    hash_code.append(f"{indent_lvl1}}}")

    return "\n".join(hash_code)


def _validate_java_identifier(name: str) -> None:
    if not name:
        raise ValueError("Field name cannot be empty")

    if name in JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS:
        raise ValueError(f"'{name}' is a Java reserved keyword")

    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
        raise ValueError(f"Invalid Java identifier: '{name}'")

