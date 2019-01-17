import unittest
from time import sleep

import pytest

from azuresearch.indexes import Index
from tests.test_helpers import get_json_file, get_fake_name


@pytest.mark.integration
def test_load_index_from_file():
    index = Index("test_index", [])
    new_index = index.load(get_json_file("hotels.index.json"))

    assert new_index.fields is not None
    assert len(new_index.fields) > 0
    assert new_index.suggesters is not None
    assert len(new_index.suggesters) > 0
    assert new_index.analyzers is not None
    assert len(new_index.analyzers) > 0


def setup_indexes():
    "Remove any indexes in the engine"
    for index in Index.list().json()['value']:
        Index(name=index['name']).delete()
    index_list = Index.list().json()
    assert len(index_list['value']) == 0


def teardown_indexes():
    for index in Index.list().json()['value']:
        Index(name=index['name']).delete()
    index_list = Index.list().json()
    assert len(index_list['value']) == 0


@pytest.mark.integration
class IndexCreate(unittest.TestCase):
    def setUp(self):
        setup_indexes()

    def tearDown(self):
        teardown_indexes()

    def test_index_create(self):
        index_list = Index.list().json()
        assert len(index_list['value']) == 0

        index = Index.load(get_json_file("hotels.index.json"))
        # print("Update index in Azure -----------------")
        result = index.update()
        #  https://docs.microsoft.com/en-us/rest/api/searchservice/create-index#response
        #  For a successful request, you should see status code "201 Created".
        assert result.status_code == 201  #

        index_list = Index.list().json()
        assert len(index_list['value']) == 1
        assert index_list['value'][0]['name'] == "hotels"


@pytest.mark.integration
class TestUpload(unittest.TestCase):
    def setUp(self):
        setup_indexes()
        hotels_index = Index.load(get_json_file("hotels.index.json"))
        name = get_fake_name()
        hotels_index.name = name
        hotels_index.update()
        hotels_index.documents.add(get_json_file("hotels.documents.json"))
        results = hotels_index.count()

        ## Wait for documents to be uploaded, then query index

        for i in range(8):
            sleep(0.5)
            count = hotels_index.count()
            print(count)
            if count == 4:
                break
        self.index = hotels_index

    def tearDown(self):
        teardown_indexes()

    def test_search(self):
        results = self.index.search("expensive").json()
        print("Results were", len(results['value']), results)
        assert len(results['value']) == 2

        results = self.index.search("memorable").json()
        print("Results were", len(results['value']), results)
        assert len(results['value']) == 1

        results = self.index.search("expensive").json()
        print("Results were", len(results['value']), results)
        assert len(results['value']) == 2


class TestBlobStorage(unittest.TestCase):
    def setUp(self):
        setup_indexes()
        hotels_index = Index.load(get_json_file("hotels.index.json"))
        name = get_fake_name()
        hotels_index.name = name
        hotels_index.update()

        self.index = hotels_index

    def tearDown(self):
        teardown_indexes()
