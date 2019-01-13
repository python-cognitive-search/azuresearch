import copy
import json

from azuresearch.indexes import Index, Field
from tests.test_helpers import get_json_file, ordered


def get_dummy_field(name, type):
    return Field(name, type)


def test_index_to_dict():
    field1 = get_dummy_field("field1", "Edm.String")
    field2 = get_dummy_field("field2", "Edm.Boolean")
    test_index = Index("test_index", [field1, field2])
    index_dict = test_index.to_dict()
    print(index_dict)
    assert index_dict['name'] == "test_index"
    assert index_dict['name'] == "test_index"
    assert index_dict['fields'] == [field1.to_dict(), field2.to_dict()]
    assert 'scoringProfiles' not in index_dict or index_dict['scoringProfiles'] == []
    assert 'suggesters' not in index_dict or index_dict['suggesters'] == []
    assert 'analyzers' not in index_dict or index_dict['analyzers'] == []
    assert 'tokenizers' not in index_dict or index_dict['tokenizers'] == []
    assert 'charFilters' not in index_dict or index_dict['charFilters'] == []
    assert 'tokenFilters' not in index_dict or index_dict['tokenFilters'] == []
    assert 'corsOptions' not in index_dict or index_dict['corsOptions'] == []


def test_index_with_no_fields_raises_exception():
    test_index = Index("test_index")


def test_load_index_correct_dict():
    expected = get_json_file("index.json")
    index_dict = copy.deepcopy(expected)
    test_index = Index.load(index_dict)
    actual = test_index.to_dict()

    expected_dump = json.dumps(expected, sort_keys=True, indent=2, )
    actual_dump = json.dumps(actual, sort_keys=True, indent=2)
    assert actual_dump == expected_dump
