import pytest

from tests.reference_data import *
from src.java_method_generator import *

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

EMPTY_NAMES = {None, ""}

MALFORMED_IDENTIFIERS = {"3", "abc-d", "gf*d"}

illegal_names = JAVA_KEYWORDS | JAVA_BUILTIN_TYPES | JAVA_LITERALS | EMPTY_NAMES | MALFORMED_IDENTIFIERS


def test_generate_getter_integer():
    attr = field_exampleAttribute_int

    assert (generate_getter(attr) == expected_getExampleAttribute_int)


def test_generate_getter_string():
    attr = field_someName_String

    assert (generate_getter(attr) == expected_getSomeName_String)


def test_generate_getter_custom_object():
    attr = field_customData_CustomObject

    assert (generate_getter(attr) == expected_getCustomData_CustomObject)


def test_generate_getter_invalid_name():
    for name in illegal_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_getter(attr)


def test_generate_setter_integer():
    attr = field_exampleAttribute_int

    assert (generate_setter(attr) == expected_setExampleAttribute_int)


def test_generate_setter_string():
    attr = field_someName_String

    assert (generate_setter(attr) == expected_setSomeName_String)


def test_generate_setter_custom_object():
    attr = field_customData_CustomObject

    assert (generate_setter(attr) == expected_setCustomData_CustomObject)


def test_generate_setter_invalid_name():
    for name in illegal_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_setter(attr)


def test_generate_getters_and_setters():
    attr1 = field_exampleAttribute_int
    attr2 = field_customData_CustomObject
    attributes = [attr1, attr2]

    expected = "\n\n".join([
        expected_getExampleAttribute_int,
        expected_setExampleAttribute_int,
        expected_getCustomData_CustomObject,
        expected_setCustomData_CustomObject
    ])
    assert generate_getters_and_setters(attributes) == expected


def test_generate_field_declaration():
    attr = field_exampleAttribute_int
    expected = """
    /**
     * javadoc description
     */
    private int exampleAttribute;"""

    assert generate_field_declaration(attr) == expected


def test_generate_field_declaration_no_description():
    attr = field_someName_String
    expected = """
    private String someName;"""

    assert generate_field_declaration(attr) == expected


def test_generate_field_declaration_invalid_name():
    for name in illegal_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_field_declaration(attr)


def test_generate_fields_block():
    attr1 = field_exampleAttribute_int
    attr2 = field_someName_String
    attr3 = field_customData_CustomObject
    attributes = [attr1, attr2, attr3]
    expected = """
    /**
     * javadoc description
     */
    private int exampleAttribute;\n
    private String someName;\n
    /**
     * another javadoc description
     */
    private CustomObject customData;"""
    assert generate_fields_block(attributes) == expected


def test_generate_hash_code():
    attr1 = field_exampleAttribute_int
    attr2 = field_someName_String
    attr3 = field_customData_CustomObject
    attributes = [attr1, attr2, attr3]
    expected = """
    @Override
    public int hashCode() {
        return Objects.hash(
                getExampleAttribute(),
                getSomeName(),
                getCustomData()
        );
    }"""
    assert generate_hash_code(attributes) == expected


def test_generate_hash_code_one_field():
    attr = field_exampleAttribute_int
    expected = """
    @Override
    public int hashCode() {
        return Objects.hash(getExampleAttribute());
    }"""
    assert generate_hash_code([attr]) == expected


def test_generate_hash_code_invalid_name():
    for name in illegal_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_hash_code([attr])


def test_generate_equals():
    class_name = "MyClass"
    attr1 = field_exampleAttribute_int
    attr2 = field_someName_String
    attr3 = field_customData_CustomObject
    attributes = [attr1, attr2, attr3]
    expected = """
    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (!(obj instanceof MyClass))
            return false;
        MyClass that = (MyClass) obj;
        return Objects.equals(getExampleAttribute(), that.getExampleAttribute())
                && Objects.equals(getSomeName(), that.getSomeName())
                && Objects.equals(getCustomData(), that.getCustomData());
    }"""
    assert generate_equals(class_name, attributes) == expected


def test_generate_equals_one_field():
    class_name = "AnotherClass"
    attr = field_someName_String
    expected = """
    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (!(obj instanceof AnotherClass))
            return false;
        AnotherClass that = (AnotherClass) obj;
        return Objects.equals(getSomeName(), that.getSomeName());
    }"""
    assert generate_equals(class_name, [attr]) == expected


def test_generate_equals_invalid_name():
    for name in illegal_names:
        attr = Field(name=name, type="String")
        with pytest.raises(ValueError):
            generate_equals("MyClass", [attr])
