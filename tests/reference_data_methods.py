from src.java_model import Field

field_exampleAttribute_int = Field(name="exampleAttribute", type="int", description="javadoc description")
field_someName_String = Field(name="someName", type="String")
field_customData_CustomObject = Field(name="customData", type="CustomObject", description="another javadoc description")
field_listOfThings_List_String = Field(name="listOfThings", type="List<String>")

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


expected_getListOfThings_list_string = """
    public List<String> getListOfThings() {
        return listOfThings;
    }"""

expected_setListOfThings_list_string = """
    public void setListOfThings(List<String> listOfThings) {
        this.listOfThings = listOfThings;
    }"""


