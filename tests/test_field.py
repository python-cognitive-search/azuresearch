import pytest

from azuresearch.indexes import Field, BooleanField, StringField, Int32Field, Int64Field, DoubleField, \
    DateTimeOffsetField, GeographyPointField
from tests.test_helpers import get_json_file, ordered


def test_field_creation_dict_correct():
    field = Field(name="test_field", type="Edm.String", index_name="test_index", searchable=True, filterable=True,
                  retrievable=True, sortable=True,
                  facetable=True,
                  key=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.String"
    assert field_dict['searchable'] == True
    assert field_dict['filterable'] == True
    assert field_dict['sortable'] == True
    assert field_dict['facetable'] == True
    assert field_dict['key'] == True
    assert field_dict['retrievable'] == True


def test_field_with_no_type_raises_exception():
    with pytest.raises(ValueError):
        Field(name="test_field",type=None)

def test_field_with_wrong_type_raises_exception():
    with pytest.raises(ValueError):
        Field(name="test_field",type="MyFunkyType")

def test_field_with_empty_name_raises_exception():
    with pytest.raises(ValueError):
        BooleanField(name="")

def test_field_with_none_name_raises_exception():
    with pytest.raises(ValueError):
        BooleanField(name=None)



def test_string_field_creation_dict_correct():
    field = StringField("test_field", sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.String"
    assert field_dict['searchable'] == True
    assert field_dict['filterable'] == True
    assert field_dict['sortable'] == False
    assert field_dict['facetable'] == True
    assert field_dict['key'] == False
    assert field_dict['retrievable'] == True


def test_int32_field_creation_dict_correct():
    field = Int32Field("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.Int32"
    assert field_dict['searchable'] == True
    assert field_dict['filterable'] == True
    assert field_dict['sortable'] == False
    assert field_dict['facetable'] == True
    assert field_dict['key'] == False
    assert field_dict['retrievable'] == True


def test_int64_field_creation_dict_correct():
    field = Int64Field("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.Int64"


def test_double_field_creation_dict_correct():
    field = DoubleField("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.Double"


def test_boolean_field_creation_dict_correct():
    field = BooleanField("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.Boolean"


def test_DateTimeOffset_field_creation_dict_correct():
    field = DateTimeOffsetField("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.DateTimeOffset"


def test_GeographyPoint_field_creation_dict_correct():
    field = GeographyPointField("test_field", searchable=True, sortable=False, retrievable=True)
    field_dict = field.to_dict()
    assert field_dict['name'] == "test_field"
    assert field_dict['type'] == "Edm.GeographyPoint"


def test_field_creation_equals_json():
    field = GeographyPointField(name="name_of_field",
                                searchable=False,
                                filterable=True,
                                sortable=True,
                                facetable=False,
                                key=False,
                                retrievable=True,
                                analyzer="name_of_analyzer_for_search_and_indexing",
                                search_analyzer="name_of_search_analyzer",
                                index_analyzer="name_of_indexing_analyzer",
                                synonym_maps=[
                                    "name_of_synonym_map"
                                ])
    actual = field.to_dict()
    expected = get_json_file("field.json")

    assert ordered(actual) == ordered(expected)
