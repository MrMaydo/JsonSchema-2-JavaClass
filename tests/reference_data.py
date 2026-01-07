from src.method_generator import Field

field_exampleAttribute_int = Field(name="exampleAttribute", type="int", description="javadoc description")
field_someName_String = Field(name="someName", type="String")
field_customData_CustomObject = Field(name="customData", type="CustomObject", description="another javadoc description")

expected_getExampleAttribute_int = """
    public int getExampleAttribute() {
        return exampleAttribute;
    }"""

expected_setExampleAttribute_int = """
    public void setExampleAttribute(int exampleAttribute) {
        this.exampleAttribute = exampleAttribute;
    }"""

expected_getSomeName_String = """
    public String getSomeName() {
        return someName;
    }"""

expected_setSomeName_String = """
    public void setSomeName(String someName) {
        this.someName = someName;
    }"""

expected_getCustomData_CustomObject = """
    public CustomObject getCustomData() {
        return customData;
    }"""

expected_setCustomData_CustomObject = """
    public void setCustomData(CustomObject customData) {
        this.customData = customData;
    }"""
