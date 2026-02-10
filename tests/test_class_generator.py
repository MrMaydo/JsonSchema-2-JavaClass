from src.class_generator import generate_java_class
from tests.reference_data_java_class import *


def test_generate_java_class():
    assert generate_java_class(class_person, package_example) == expected_java_class_person


def test_generate_java_class_no_fields():
    assert generate_java_class(class_heartbeat, package_example) == expected_java_class_heartbeat
