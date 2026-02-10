from src.java_model import Field, JavaClass

package_example = "expected.DataTypes"
field_name_string = Field(name="name", type="String", description="This contains name.")
field_age_int = Field(name="age", type="int", description="This contains age.")
field_birthdate_date = Field(name="birthDate", type="Date")
field_additionalInfo_CustomObject = Field(name="additionalInfo", type="CustomData")

person_class_fields = [field_name_string, field_age_int, field_birthdate_date, field_additionalInfo_CustomObject]

class_person = JavaClass(name="Person", fields=person_class_fields, description="Contains information about a person.")
class_heartbeat = JavaClass(name="Heartbeat", fields=[])

expected_java_class_person = """\
package expected.DataTypes;


import java.util.Date;
import java.util.Objects;


/**
 * Contains information about a person.
 */
public class Person {

    /**
     * This contains name.
     */
    private String name;

    /**
     * This contains age.
     */
    private int age;

    private Date birthDate;

    private CustomData additionalInfo;


    public String getName() {
        return name;
    }


    public void setName(String name) {
        this.name = name;
    }


    public int getAge() {
        return age;
    }


    public void setAge(int age) {
        this.age = age;
    }


    public Date getBirthDate() {
        return birthDate;
    }


    public void setBirthDate(Date birthDate) {
        this.birthDate = birthDate;
    }


    public CustomData getAdditionalInfo() {
        return additionalInfo;
    }


    public void setAdditionalInfo(CustomData additionalInfo) {
        this.additionalInfo = additionalInfo;
    }


    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (!(obj instanceof Person))
            return false;
        Person that = (Person) obj;
        return Objects.equals(getName(), that.getName())
                && Objects.equals(getAge(), that.getAge())
                && Objects.equals(getBirthDate(), that.getBirthDate())
                && Objects.equals(getAdditionalInfo(), that.getAdditionalInfo());
    }


    @Override
    public int hashCode() {
        return Objects.hash(
                getName(),
                getAge(),
                getBirthDate(),
                getAdditionalInfo()
        );
    }
}
"""

expected_java_class_heartbeat = """\
package expected.DataTypes;


public class Heartbeat {
}
"""
