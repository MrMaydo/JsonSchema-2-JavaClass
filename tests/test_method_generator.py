import pytest

from src.method_generator import generate_getter, Field

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


def test_generate_getter_integer():
    attr = Field(
        name="exampleAttribute",
        type="Integer"
    )
    expected = """
    public Integer getExampleAttribute() {
        return exampleAttribute;
    }
    """
    assert (generate_getter(attr) == expected)


def test_generate_getter_string():
    attr = Field(name="someName", type="String")
    expected = """
    public String getSomeName() {
        return someName;
    }
    """
    assert (generate_getter(attr) == expected)


def test_generate_getter_invalid_name():
    EMPTY_NAMES = {None, ""}
    invalid_names = JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS | EMPTY_NAMES
    for name in invalid_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_getter(attr)

