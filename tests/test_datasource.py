import copy

from azuresearch.data_source import DataSource
from tests.test_helpers import get_json_file, ordered


def test_field_creation_equals_json():

    expected = get_json_file("datasource.json")
    datasource_dict = copy.deepcopy(expected)
    datasource = DataSource.load(datasource_dict)
    actual = datasource.to_dict()

    assert ordered(actual) == ordered(expected)
