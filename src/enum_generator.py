import re


def to_java_constant(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]", "_", value)  # delimiters a-a -> A_A
    value = re.sub(r"([a-z])[_]?([A-Z])([A-Z])([a-z])", r"\1_\2_\3\4", value)  # aBCd / a_BCd-> a_B_CD
    value = re.sub(r"([a-z])([A-Z])", r"\1_\2", value)  # aA -> A_A
    value = re.sub(r"([A-Za-z])([0-9])", r"\1_\2", value)  # a9 / A9 -> a_9
    value = re.sub(r"([0-9])([A-Za-z])", r"\1_\2", value)  # 9a / 9A -> 9_A

    return value.upper()
