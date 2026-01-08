from src.enum_generator import EnumClass

enum_AttributeEnum = EnumClass(
    name="AttributeEnum",
    values=["Actual", "Target", "MinSet", "MaxSet"],
    description="Type of attribute: Actual, Target, MinSet, MaxSet.")

enum_CancelReservationStatusEnum = EnumClass(
    name="CancelReservationStatusEnum",
    values=["Accepted"])

expected_AttributeEnum = """package ocpp.msgDef.Enumerations;

import java.util.HashMap;
import java.util.Map;


/**
 * Type of attribute: Actual, Target, MinSet, MaxSet.
 */
public enum AttributeEnum {
    ACTUAL("Actual"),
    TARGET("Target"),
    MIN_SET("MinSet"),
    MAX_SET("MaxSet");

    private final static Map<String, AttributeEnum> CONSTANTS = new HashMap<String, AttributeEnum>();

    static {
        for (AttributeEnum c : values()) {
            CONSTANTS.put(c.value, c);
        }
    }

    private final String value;

    AttributeEnum(String value) {
        this.value = value;
    }

    public static AttributeEnum fromValue(String value) {
        AttributeEnum constant = CONSTANTS.get(value);
        if (constant == null) {
            throw new IllegalArgumentException(value);
        } else {
            return constant;
        }
    }

    @Override
    public String toString() {
        return this.value;
    }

    public String value() {
        return this.value;
    }
}
"""

expected_CancelReservationStatusEnum = """package ocpp.anotherDef.Enums;

import java.util.HashMap;
import java.util.Map;


public enum CancelReservationStatusEnum {
    ACCEPTED("Accepted");

    private final static Map<String, CancelReservationStatusEnum> CONSTANTS = new HashMap<String, CancelReservationStatusEnum>();

    static {
        for (CancelReservationStatusEnum c : values()) {
            CONSTANTS.put(c.value, c);
        }
    }

    private final String value;

    CancelReservationStatusEnum(String value) {
        this.value = value;
    }

    public static CancelReservationStatusEnum fromValue(String value) {
        CancelReservationStatusEnum constant = CONSTANTS.get(value);
        if (constant == null) {
            throw new IllegalArgumentException(value);
        } else {
            return constant;
        }
    }

    @Override
    public String toString() {
        return this.value;
    }

    public String value() {
        return this.value;
    }
}
"""
