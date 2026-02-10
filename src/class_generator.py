from src.header_generator import set_package, set_imports, render_javadoc
from src.java_method_generator import generate_fields_block, generate_getters_and_setters, generate_equals, \
    generate_hash_code
from src.java_model import JavaClass


def generate_java_class(java_class: JavaClass, package: str) -> str:
    if len(java_class.fields) == 0:
        return _empty_java_class(java_class, package)

    body = [
        set_package(package),
        "",
        "",
        set_imports(java_class.fields),
        "",
        render_javadoc(java_class.description, indent_lvl=0),
        f"public class {java_class.name} {{",
        generate_fields_block(java_class.fields),
        "",
        generate_getters_and_setters(java_class.fields),
        "",
        generate_equals(java_class.name, java_class.fields),
        "",
        generate_hash_code(java_class.fields),
        "}",
        ""
    ]
    return "\n".join(body)


def _empty_java_class(java_class: JavaClass, package: str) -> str:
    body = [
        set_package(package),
        "",
        render_javadoc(java_class.description, indent_lvl=0),
        f"public class {java_class.name} {{",
        "}",
        ""
    ]
    return "\n".join(body)
