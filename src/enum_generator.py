import re
from dataclasses import dataclass
from typing import List, Optional

from src.header_generator import set_package


@dataclass
class EnumClass:
    name: str
    values: List[str]
    description: Optional[str] = None


indent_lvl1 = "    "
indent_lvl2 = indent_lvl1 * 2
indent_lvl3 = indent_lvl1 * 3


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
        f""
        ]

    enum_body.extend(_get_javadoc(enum_class.description))

    enum_body.append(f"public enum {enum_class.name} {{")
    enum_body.extend(_get_constants(enum_class.values))

    enum_body.append(f"")
    enum_body.append(f"{indent_lvl1}private final static Map<String, {enum_class.name}> CONSTANTS = new HashMap<String, {enum_class.name}>();")
    enum_body.append(f"")
    enum_body.extend(_get_static_method(enum_class.name))

    enum_body.append(f"")
    enum_body.append(f"{indent_lvl1}private final String value;")
    enum_body.append(f"")
    enum_body.extend(_get_constructor(enum_class.name))

    enum_body.append(f"")
    enum_body.extend(_get_fromValue_method(enum_class.name))

    enum_body.append(f"")
    enum_body.extend(_get_toString_method())

    enum_body.append(f"")
    enum_body.extend(_get_value_method())
    enum_body.append("}")
    enum_body.append(f"")

    return "\n".join(enum_body)


def _get_javadoc(description: str) -> List[str]:
    javadoc = [""]
    if description is not None:
        javadoc = [
            "",
            "/**",
            f" * {description}",
            " */"
        ]
    return javadoc


def _get_constants(constants: List[str]) -> List[str]:
    values = []
    for i, value in enumerate(constants):
        line_end = ";" if i == (len(constants) - 1) else ","
        values.append(
            f'{indent_lvl1}{to_java_constant(value)}("{value}"){line_end}'
        )
    return values


def _get_static_method(class_name: str) -> List[str]:
    body = [
        f"{indent_lvl1}static {{",
        f"{indent_lvl2}for ({class_name} c : values()) {{",
        f"{indent_lvl3}CONSTANTS.put(c.value, c);",
        f"{indent_lvl2}}}",
        f"{indent_lvl1}}}"
    ]
    return body


def _get_constructor(class_name: str) -> List[str]:
    body = [
        f"{indent_lvl1}{class_name}(String value) {{",
        f"{indent_lvl2}this.value = value;",
        f"{indent_lvl1}}}"
    ]
    return body


def _get_fromValue_method(class_name: str) -> List[str]:
    body = [
        f"{indent_lvl1}public static {class_name} fromValue(String value) {{",
        f"{indent_lvl2}{class_name} constant = CONSTANTS.get(value);",
        f"{indent_lvl2}if (constant == null) {{",
        f"{indent_lvl3}throw new IllegalArgumentException(value);",
        f"{indent_lvl2}}} else {{",
        f"{indent_lvl3}return constant;",
        f"{indent_lvl2}}}",
        f"{indent_lvl1}}}"
    ]
    return body


def _get_toString_method() -> List[str]:
    body = [
        f"{indent_lvl1}@Override",
        f"{indent_lvl1}public String toString() {{",
        f"{indent_lvl2}return this.value;",
        f"{indent_lvl1}}}"
    ]
    return body


def _get_value_method() -> List[str]:
    body = [
        f"{indent_lvl1}public String value() {{",
        f"{indent_lvl2}return this.value;",
        f"{indent_lvl1}}}"
    ]
    return body
