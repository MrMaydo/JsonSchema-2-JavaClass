import re
from typing import List

from src.header_generator import set_package, render_javadoc
from src.java_model import EnumClass, indent


def to_java_constant(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]", "_", value)  # delimiters a-a -> A_A
    value = re.sub(r"([a-z])[_]?([A-Z])([A-Z])([a-z])", r"\1_\2_\3\4", value)  # aBCd / a_BCd-> a_B_CD
    value = re.sub(r"([a-z])([A-Z])", r"\1_\2", value)  # aA -> A_A
    value = re.sub(r"([A-Za-z])([0-9])", r"\1_\2", value)  # a9 / A9 -> a_9
    value = re.sub(r"([0-9])([A-Za-z])", r"\1_\2", value)  # 9a / 9A -> 9_A

    return value.upper()


def generate_enum_class(enum_class: EnumClass, package: str) -> str:
    enum_body = [
        set_package(package),
        "",
        f"import java.util.HashMap;",
        f"import java.util.Map;",
        f"",
        render_javadoc(enum_class.description, indent_lvl=0),
        f"public enum {enum_class.name} {{",
        _get_constants(enum_class.values),
        f"",
        f"{indent(1)}private final static Map<String, {enum_class.name}> CONSTANTS = new HashMap<String, {enum_class.name}>();",
        _get_static_method(enum_class.name),
        f"",
        f"{indent(1)}private final String value;",
        _get_constructor(enum_class.name),
        _get_from_value_method(enum_class.name),
        _get_to_string_method(),
        _get_value_method(),
        "}",
        f""
    ]

    return "\n".join(enum_body)


def _get_constants(constants: List[str]) -> str:
    values = []
    for i, value in enumerate(constants):
        line_end = ";" if i == (len(constants) - 1) else ","
        values.append(
            f'{indent(1)}{to_java_constant(value)}("{value}"){line_end}'
        )
    return "\n".join(values)


def _get_static_method(class_name: str) -> str:
    body = [
        "",
        f"{indent(1)}static {{",
        f"{indent(2)}for ({class_name} c : values()) {{",
        f"{indent(3)}CONSTANTS.put(c.value, c);",
        f"{indent(2)}}}",
        f"{indent(1)}}}"
    ]
    return "\n".join(body)


def _get_constructor(class_name: str) -> str:
    body = [
        "",
        f"{indent(1)}{class_name}(String value) {{",
        f"{indent(2)}this.value = value;",
        f"{indent(1)}}}"
    ]
    return "\n".join(body)


def _get_from_value_method(class_name: str) -> str:
    body = [
        "",
        f"{indent(1)}public static {class_name} fromValue(String value) {{",
        f"{indent(2)}{class_name} constant = CONSTANTS.get(value);",
        f"{indent(2)}if (constant == null) {{",
        f"{indent(3)}throw new IllegalArgumentException(value);",
        f"{indent(2)}}} else {{",
        f"{indent(3)}return constant;",
        f"{indent(2)}}}",
        f"{indent(1)}}}"
    ]
    return "\n".join(body)


def _get_to_string_method() -> str:
    body = [
        "",
        f"{indent(1)}@Override",
        f"{indent(1)}public String toString() {{",
        f"{indent(2)}return this.value;",
        f"{indent(1)}}}"
    ]
    return "\n".join(body)


def _get_value_method() -> str:
    body = [
        "",
        f"{indent(1)}public String value() {{",
        f"{indent(2)}return this.value;",
        f"{indent(1)}}}"
    ]
    return "\n".join(body)
