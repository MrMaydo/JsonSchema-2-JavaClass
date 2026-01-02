import pytest

from src.header_generator import set_package


def test_set_package():
    example = "org.example.hyphenated_name"
    expected = f"package {example}"
    assert set_package(example) == expected

    example_2 = "com.example._123name"
    expected_2 = f"package {example_2}"
    assert set_package(example_2) == expected_2


def test_set_package_illegal_name():
    example = "org.example.hyphenated-name"
    with pytest.raises(ValueError):
        set_package(example)

    example_2 = "com.example.123name"
    with pytest.raises(ValueError):
        set_package(example_2)
