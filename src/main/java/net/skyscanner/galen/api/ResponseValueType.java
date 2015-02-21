/**
 * Autogenerated by Thrift Compiler (0.9.2)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
package net.skyscanner.galen.api;

import org.apache.thrift.scheme.IScheme;
import org.apache.thrift.scheme.SchemeFactory;
import org.apache.thrift.scheme.StandardScheme;

import org.apache.thrift.scheme.TupleScheme;
import org.apache.thrift.protocol.TTupleProtocol;
import org.apache.thrift.protocol.TProtocolException;
import org.apache.thrift.EncodingUtils;
import org.apache.thrift.TException;
import org.apache.thrift.async.AsyncMethodCallback;
import org.apache.thrift.server.AbstractNonblockingServer.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.EnumMap;
import java.util.Set;
import java.util.HashSet;
import java.util.EnumSet;
import java.util.Collections;
import java.util.BitSet;
import java.nio.ByteBuffer;
import java.util.Arrays;
import javax.annotation.Generated;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SuppressWarnings({"cast", "rawtypes", "serial", "unchecked"})
public class ResponseValueType extends org.apache.thrift.TUnion<ResponseValueType, ResponseValueType._Fields> {
  private static final org.apache.thrift.protocol.TStruct STRUCT_DESC = new org.apache.thrift.protocol.TStruct("ResponseValueType");
  private static final org.apache.thrift.protocol.TField STRING_CAP_FIELD_DESC = new org.apache.thrift.protocol.TField("string_cap", org.apache.thrift.protocol.TType.STRING, (short)1);
  private static final org.apache.thrift.protocol.TField BOOL_CAP_FIELD_DESC = new org.apache.thrift.protocol.TField("bool_cap", org.apache.thrift.protocol.TType.BOOL, (short)2);
  private static final org.apache.thrift.protocol.TField SET_CAP_FIELD_DESC = new org.apache.thrift.protocol.TField("set_cap", org.apache.thrift.protocol.TType.SET, (short)3);

  /** The set of fields this struct contains, along with convenience methods for finding and manipulating them. */
  public enum _Fields implements org.apache.thrift.TFieldIdEnum {
    STRING_CAP((short)1, "string_cap"),
    BOOL_CAP((short)2, "bool_cap"),
    SET_CAP((short)3, "set_cap");

    private static final Map<String, _Fields> byName = new HashMap<String, _Fields>();

    static {
      for (_Fields field : EnumSet.allOf(_Fields.class)) {
        byName.put(field.getFieldName(), field);
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, or null if its not found.
     */
    public static _Fields findByThriftId(int fieldId) {
      switch(fieldId) {
        case 1: // STRING_CAP
          return STRING_CAP;
        case 2: // BOOL_CAP
          return BOOL_CAP;
        case 3: // SET_CAP
          return SET_CAP;
        default:
          return null;
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, throwing an exception
     * if it is not found.
     */
    public static _Fields findByThriftIdOrThrow(int fieldId) {
      _Fields fields = findByThriftId(fieldId);
      if (fields == null) throw new IllegalArgumentException("Field " + fieldId + " doesn't exist!");
      return fields;
    }

    /**
     * Find the _Fields constant that matches name, or null if its not found.
     */
    public static _Fields findByName(String name) {
      return byName.get(name);
    }

    private final short _thriftId;
    private final String _fieldName;

    _Fields(short thriftId, String fieldName) {
      _thriftId = thriftId;
      _fieldName = fieldName;
    }

    public short getThriftFieldId() {
      return _thriftId;
    }

    public String getFieldName() {
      return _fieldName;
    }
  }

  public static final Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> metaDataMap;
  static {
    Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> tmpMap = new EnumMap<_Fields, org.apache.thrift.meta_data.FieldMetaData>(_Fields.class);
    tmpMap.put(_Fields.STRING_CAP, new org.apache.thrift.meta_data.FieldMetaData("string_cap", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
    tmpMap.put(_Fields.BOOL_CAP, new org.apache.thrift.meta_data.FieldMetaData("bool_cap", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.BOOL)));
    tmpMap.put(_Fields.SET_CAP, new org.apache.thrift.meta_data.FieldMetaData("set_cap", org.apache.thrift.TFieldRequirementType.DEFAULT, 
        new org.apache.thrift.meta_data.SetMetaData(org.apache.thrift.protocol.TType.SET, 
            new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING))));
    metaDataMap = Collections.unmodifiableMap(tmpMap);
    org.apache.thrift.meta_data.FieldMetaData.addStructMetaDataMap(ResponseValueType.class, metaDataMap);
  }

  public ResponseValueType() {
    super();
  }

  public ResponseValueType(_Fields setField, Object value) {
    super(setField, value);
  }

  public ResponseValueType(ResponseValueType other) {
    super(other);
  }
  public ResponseValueType deepCopy() {
    return new ResponseValueType(this);
  }

  public static ResponseValueType string_cap(String value) {
    ResponseValueType x = new ResponseValueType();
    x.setString_cap(value);
    return x;
  }

  public static ResponseValueType bool_cap(boolean value) {
    ResponseValueType x = new ResponseValueType();
    x.setBool_cap(value);
    return x;
  }

  public static ResponseValueType set_cap(Set<String> value) {
    ResponseValueType x = new ResponseValueType();
    x.setSet_cap(value);
    return x;
  }


  @Override
  protected void checkType(_Fields setField, Object value) throws ClassCastException {
    switch (setField) {
      case STRING_CAP:
        if (value instanceof String) {
          break;
        }
        throw new ClassCastException("Was expecting value of type String for field 'string_cap', but got " + value.getClass().getSimpleName());
      case BOOL_CAP:
        if (value instanceof Boolean) {
          break;
        }
        throw new ClassCastException("Was expecting value of type Boolean for field 'bool_cap', but got " + value.getClass().getSimpleName());
      case SET_CAP:
        if (value instanceof Set) {
          break;
        }
        throw new ClassCastException("Was expecting value of type Set<String> for field 'set_cap', but got " + value.getClass().getSimpleName());
      default:
        throw new IllegalArgumentException("Unknown field id " + setField);
    }
  }

  @Override
  protected Object standardSchemeReadValue(org.apache.thrift.protocol.TProtocol iprot, org.apache.thrift.protocol.TField field) throws TException {
    _Fields setField = _Fields.findByThriftId(field.id);
    if (setField != null) {
      switch (setField) {
        case STRING_CAP:
          if (field.type == STRING_CAP_FIELD_DESC.type) {
            String string_cap;
            string_cap = iprot.readString();
            return string_cap;
          } else {
            org.apache.thrift.protocol.TProtocolUtil.skip(iprot, field.type);
            return null;
          }
        case BOOL_CAP:
          if (field.type == BOOL_CAP_FIELD_DESC.type) {
            Boolean bool_cap;
            bool_cap = iprot.readBool();
            return bool_cap;
          } else {
            org.apache.thrift.protocol.TProtocolUtil.skip(iprot, field.type);
            return null;
          }
        case SET_CAP:
          if (field.type == SET_CAP_FIELD_DESC.type) {
            Set<String> set_cap;
            {
              org.apache.thrift.protocol.TSet _set0 = iprot.readSetBegin();
              set_cap = new HashSet<String>(2*_set0.size);
              String _elem1;
              for (int _i2 = 0; _i2 < _set0.size; ++_i2)
              {
                _elem1 = iprot.readString();
                set_cap.add(_elem1);
              }
              iprot.readSetEnd();
            }
            return set_cap;
          } else {
            org.apache.thrift.protocol.TProtocolUtil.skip(iprot, field.type);
            return null;
          }
        default:
          throw new IllegalStateException("setField wasn't null, but didn't match any of the case statements!");
      }
    } else {
      org.apache.thrift.protocol.TProtocolUtil.skip(iprot, field.type);
      return null;
    }
  }

  @Override
  protected void standardSchemeWriteValue(org.apache.thrift.protocol.TProtocol oprot) throws TException {
    switch (setField_) {
      case STRING_CAP:
        String string_cap = (String)value_;
        oprot.writeString(string_cap);
        return;
      case BOOL_CAP:
        Boolean bool_cap = (Boolean)value_;
        oprot.writeBool(bool_cap);
        return;
      case SET_CAP:
        Set<String> set_cap = (Set<String>)value_;
        {
          oprot.writeSetBegin(new org.apache.thrift.protocol.TSet(org.apache.thrift.protocol.TType.STRING, set_cap.size()));
          for (String _iter3 : set_cap)
          {
            oprot.writeString(_iter3);
          }
          oprot.writeSetEnd();
        }
        return;
      default:
        throw new IllegalStateException("Cannot write union with unknown field " + setField_);
    }
  }

  @Override
  protected Object tupleSchemeReadValue(org.apache.thrift.protocol.TProtocol iprot, short fieldID) throws TException {
    _Fields setField = _Fields.findByThriftId(fieldID);
    if (setField != null) {
      switch (setField) {
        case STRING_CAP:
          String string_cap;
          string_cap = iprot.readString();
          return string_cap;
        case BOOL_CAP:
          Boolean bool_cap;
          bool_cap = iprot.readBool();
          return bool_cap;
        case SET_CAP:
          Set<String> set_cap;
          {
            org.apache.thrift.protocol.TSet _set4 = iprot.readSetBegin();
            set_cap = new HashSet<String>(2*_set4.size);
            String _elem5;
            for (int _i6 = 0; _i6 < _set4.size; ++_i6)
            {
              _elem5 = iprot.readString();
              set_cap.add(_elem5);
            }
            iprot.readSetEnd();
          }
          return set_cap;
        default:
          throw new IllegalStateException("setField wasn't null, but didn't match any of the case statements!");
      }
    } else {
      throw new TProtocolException("Couldn't find a field with field id " + fieldID);
    }
  }

  @Override
  protected void tupleSchemeWriteValue(org.apache.thrift.protocol.TProtocol oprot) throws TException {
    switch (setField_) {
      case STRING_CAP:
        String string_cap = (String)value_;
        oprot.writeString(string_cap);
        return;
      case BOOL_CAP:
        Boolean bool_cap = (Boolean)value_;
        oprot.writeBool(bool_cap);
        return;
      case SET_CAP:
        Set<String> set_cap = (Set<String>)value_;
        {
          oprot.writeSetBegin(new org.apache.thrift.protocol.TSet(org.apache.thrift.protocol.TType.STRING, set_cap.size()));
          for (String _iter7 : set_cap)
          {
            oprot.writeString(_iter7);
          }
          oprot.writeSetEnd();
        }
        return;
      default:
        throw new IllegalStateException("Cannot write union with unknown field " + setField_);
    }
  }

  @Override
  protected org.apache.thrift.protocol.TField getFieldDesc(_Fields setField) {
    switch (setField) {
      case STRING_CAP:
        return STRING_CAP_FIELD_DESC;
      case BOOL_CAP:
        return BOOL_CAP_FIELD_DESC;
      case SET_CAP:
        return SET_CAP_FIELD_DESC;
      default:
        throw new IllegalArgumentException("Unknown field id " + setField);
    }
  }

  @Override
  protected org.apache.thrift.protocol.TStruct getStructDesc() {
    return STRUCT_DESC;
  }

  @Override
  protected _Fields enumForId(short id) {
    return _Fields.findByThriftIdOrThrow(id);
  }

  public _Fields fieldForId(int fieldId) {
    return _Fields.findByThriftId(fieldId);
  }


  public String getString_cap() {
    if (getSetField() == _Fields.STRING_CAP) {
      return (String)getFieldValue();
    } else {
      throw new RuntimeException("Cannot get field 'string_cap' because union is currently set to " + getFieldDesc(getSetField()).name);
    }
  }

  public void setString_cap(String value) {
    if (value == null) throw new NullPointerException();
    setField_ = _Fields.STRING_CAP;
    value_ = value;
  }

  public boolean getBool_cap() {
    if (getSetField() == _Fields.BOOL_CAP) {
      return (Boolean)getFieldValue();
    } else {
      throw new RuntimeException("Cannot get field 'bool_cap' because union is currently set to " + getFieldDesc(getSetField()).name);
    }
  }

  public void setBool_cap(boolean value) {
    setField_ = _Fields.BOOL_CAP;
    value_ = value;
  }

  public Set<String> getSet_cap() {
    if (getSetField() == _Fields.SET_CAP) {
      return (Set<String>)getFieldValue();
    } else {
      throw new RuntimeException("Cannot get field 'set_cap' because union is currently set to " + getFieldDesc(getSetField()).name);
    }
  }

  public void setSet_cap(Set<String> value) {
    if (value == null) throw new NullPointerException();
    setField_ = _Fields.SET_CAP;
    value_ = value;
  }

  public boolean isSetString_cap() {
    return setField_ == _Fields.STRING_CAP;
  }


  public boolean isSetBool_cap() {
    return setField_ == _Fields.BOOL_CAP;
  }


  public boolean isSetSet_cap() {
    return setField_ == _Fields.SET_CAP;
  }


  public boolean equals(Object other) {
    if (other instanceof ResponseValueType) {
      return equals((ResponseValueType)other);
    } else {
      return false;
    }
  }

  public boolean equals(ResponseValueType other) {
    return other != null && getSetField() == other.getSetField() && getFieldValue().equals(other.getFieldValue());
  }

  @Override
  public int compareTo(ResponseValueType other) {
    int lastComparison = org.apache.thrift.TBaseHelper.compareTo(getSetField(), other.getSetField());
    if (lastComparison == 0) {
      return org.apache.thrift.TBaseHelper.compareTo(getFieldValue(), other.getFieldValue());
    }
    return lastComparison;
  }


  @Override
  public int hashCode() {
    List<Object> list = new ArrayList<Object>();
    list.add(this.getClass().getName());
    org.apache.thrift.TFieldIdEnum setField = getSetField();
    if (setField != null) {
      list.add(setField.getThriftFieldId());
      Object value = getFieldValue();
      if (value instanceof org.apache.thrift.TEnum) {
        list.add(((org.apache.thrift.TEnum)getFieldValue()).getValue());
      } else {
        list.add(value);
      }
    }
    return list.hashCode();
  }
  private void writeObject(java.io.ObjectOutputStream out) throws java.io.IOException {
    try {
      write(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(out)));
    } catch (TException te) {
      throw new java.io.IOException(te);
    }
  }


  private void readObject(java.io.ObjectInputStream in) throws java.io.IOException, ClassNotFoundException {
    try {
      read(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(in)));
    } catch (TException te) {
      throw new java.io.IOException(te);
    }
  }


}
