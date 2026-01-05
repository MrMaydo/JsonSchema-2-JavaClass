from src.enum_generator import to_java_constant


def test_to_java_constant():
    values_expected = {
        "kit": "KIT",
        "KIT": "KIT",
        "kitKat": "KIT_KAT",
        "KitKat": "KIT_KAT",
        "kit-kat": "KIT_KAT",
        "kit-Kat": "KIT_KAT",
        "kit_kat": "KIT_KAT",
        "kit_Kat": "KIT_KAT",
        "kit9": "KIT_9",
        "kit-9": "KIT_9",
        "kit_9": "KIT_9",
        "kit92": "KIT_92",
        "KiT": "KI_T",
        "KiTKat": "KI_T_KAT",
        "KitKAT": "KIT_KAT"
    }
    for key in values_expected.keys():
        assert to_java_constant(key) == values_expected[key]
