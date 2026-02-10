import pytest

from src.java_model import Field
from src.header_generator import set_package, set_imports, render_javadoc


def test_set_package():
    example = "org.example.hyphenated_name"
    expected = f"package {example};"
    assert set_package(example) == expected

    example_2 = "com.example._123name"
    expected_2 = f"package {example_2};"
    assert set_package(example_2) == expected_2

    example_3 = "com.exAmple.Name"
    expected_3 = f"package {example_3};"
    assert set_package(example_3) == expected_3


def test_set_package_illegal_name():
    example = "org.example.hyphenated-name"
    with pytest.raises(ValueError):
        set_package(example)

    example_2 = "com.example.123name"
    with pytest.raises(ValueError):
        set_package(example_2)


def test_set_imports_all():
    field_date = Field(name="birthDate", type="Date")
    field_string = Field(name="birthDate", type="String")
    field_list = Field(name="setOfSth", type="List")
    fields = [field_list, field_string, field_date]
    expected = """\
import java.util.Date;
import java.util.List;
import java.util.Objects;"""
    assert set_imports(fields) == expected


def test_set_imports_individual_import():
    field_date = Field(name="birthDate", type="Date")
    fields = [field_date]
    expected = """\
import java.util.Date;
import java.util.Objects;"""
    assert set_imports(fields) == expected


def test_set_imports_no_additional_imports():
    field_int = Field(name="age", type="int")
    fields = [field_int]
    expected = """\
import java.util.Objects;"""
    assert set_imports(fields) == expected


def test_render_javadoc_class_indent():
    description = "Example class description"
    expected = """
/**
 * Example class description
 */"""
    assert render_javadoc(description, 0) == expected


def test_render_javadoc_field_indent():
    description = "Example field description"
    expected = """
    /**
     * Example field description
     */"""
    assert render_javadoc(description, 1) == expected


def test_render_javadoc_no_description():
    assert render_javadoc("", 0) == ""
    assert render_javadoc(None, 0) == ""
    assert render_javadoc(None, 1) == ""
