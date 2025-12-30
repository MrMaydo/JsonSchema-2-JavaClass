import pytest

from src.method_generator import generate_getter, Field, generate_setter, generate_getters_and_setters

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
        type="int"
    )
    expected = """
    public int getExampleAttribute() {
        return exampleAttribute;
    }"""
    assert (generate_getter(attr) == expected)


def test_generate_getter_string():
    attr = Field(name="someName", type="String")
    expected = """
    public String getSomeName() {
        return someName;
    }"""
    assert (generate_getter(attr) == expected)


def test_generate_getter_custom_object():
    attr = Field(name="customData", type="CustomObject")
    expected = """
    public CustomObject getCustomData() {
        return customData;
    }"""
    assert (generate_getter(attr) == expected)


def test_generate_getter_invalid_name():
    EMPTY_NAMES = {None, ""}
    invalid_names = JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS | EMPTY_NAMES | {"3", "abc-d"}
    for name in invalid_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_getter(attr)


def test_generate_setter_integer():
    attr = Field(name="exampleAttribute", type="int")
    expected = """
    public void setExampleAttribute(int exampleAttribute) {
        this.exampleAttribute = exampleAttribute;
    }"""
    assert (generate_setter(attr) == expected)


def test_generate_setter_string():
    attr = Field(name="someName", type="String")
    expected = """
    public void setSomeName(String someName) {
        this.someName = someName;
    }"""
    assert (generate_setter(attr) == expected)


def test_generate_setter_custom_object():
    attr = Field(name="customData", type="CustomObject")
    expected = """
    public void setCustomData(CustomObject customData) {
        this.customData = customData;
    }"""
    assert (generate_setter(attr) == expected)


def test_generate_setter_invalid_name():
    EMPTY_NAMES = {None, ""}
    invalid_names = JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS | EMPTY_NAMES | {"9", "gf*d"}
    for name in invalid_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_setter(attr)


def test_generate_getters_and_setters():
    attr1 = Field(name="exampleAttribute", type="int")
    attr2 = Field(name="customData", type="CustomObject")
    attributes = [attr1, attr2]
    expected = """
    public int getExampleAttribute() {
        return exampleAttribute;
    }\n\n
    public void setExampleAttribute(int exampleAttribute) {
        this.exampleAttribute = exampleAttribute;
    }\n\n
    public CustomObject getCustomData() {
        return customData;
    }\n\n
    public void setCustomData(CustomObject customData) {
        this.customData = customData;
    }"""
    assert generate_getters_and_setters(attributes) == expected
