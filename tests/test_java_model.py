import pytest

from src.java_model import indent


def test_indent_zero():
    assert indent(0) == ""


def test_indent_default_size():
    assert indent(1) == " " * 4


def test_indent_multiple_levels():
    assert indent(3) == " " * 12


def test_indent_custom_size():
    assert indent(2, size=2) == " " * 4


def test_indent_size_zero():
    assert indent(5, size=0) == ""


def test_indent_negative_lvl():
    with pytest.raises(ValueError):
        indent(level=-1, size=4)


def test_indent_negative_size():
    with pytest.raises(ValueError):
        indent(level=1, size=-1)
