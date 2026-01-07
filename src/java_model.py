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
indent_lvl1 = " " * 4
indent_lvl2 = indent_lvl1 * 2
indent_lvl3 = indent_lvl1 * 3
return_indent = "        "


@dataclass
class EnumClass:
    name: str
    values: List[str]
    description: Optional[str] = None


@dataclass
class Field:
    name: str
    type: str
    description: Optional[str] = None
