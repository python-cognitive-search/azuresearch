import os
import time

import pytest

from azuresearch.data_source import DataSource
from azuresearch.field_mapping import FieldMapping
from azuresearch.indexers.indexer import Indexer
from azuresearch.indexes import StringField, Index, Int64Field, \
    DateTimeOffsetField
from tests.test_helpers import get_json_file

path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.integration
def test_another_pipeline():
    # create datasource.
    # json holds the datasource params (name, connection string etc.)

    config = get_json_file("blob_config.json", path=path, dir=None)
    datasource = DataSource.load(config)
    # delete the data source to to support quick iterations
    datasource.delete_if_exists()
    datasource.create()

    # define fields and index
    field1 = StringField("id", key=True, sortable=True)
    field2 = StringField("url")
    field3 = StringField("file_name", sortable=False)
    field4 = StringField("content", searchable=True)
    field5 = Int64Field("size", sortable=True)
    field6 = DateTimeOffsetField("last_modified", sortable=True)

    fields = [field1, field2, field3, field4, field5, field6]

    index = Index("my-index", fields=fields)
    index.delete_if_exists()
    index.create()

    # Define field mappings and indexer

    f_m1 = FieldMapping(source_field_name='metadata_storage_path',
                        target_field_name='id',
                        mapping_function={"name": "base64Encode"})
    f_m2 = FieldMapping(source_field_name='metadata_storage_path',
                        target_field_name='url')
    f_m3 = FieldMapping(source_field_name='metadata_storage_name',
                        target_field_name='file_name')
    f_m4 = FieldMapping(source_field_name='content',
                        target_field_name='content')
    f_m5 = FieldMapping(source_field_name='metadata_storage_size',
                        target_field_name='size')
    f_m6 = FieldMapping(source_field_name='metadata_storage_last_modified',
                        target_field_name='last_modified')

    indexer = Indexer(name="my-indexer",
                      data_source_name="ohblob",
                      target_index_name='my-index',
                      skillset_name=None,
                      field_mappings=[f_m1, f_m2, f_m3, f_m4, f_m5, f_m6])
    print(indexer.to_dict())

    indexer.delete_if_exists()
    indexer.create()

    indexer_status = ""
    last_run_status = None
    while indexer_status != "error" and (
            last_run_status is None or last_run_status == "inProgress"):
        status = indexer.get_status()
        indexer_status = status.get("status")
        last_run_status = status.get("lastResult")
        if last_run_status is not None:
            last_run_status = last_run_status.get("status")
            print("last run status: " + last_run_status)

        print("indexer status is: " + indexer_status)
        time.sleep(3)  # wait for 3 seconds until rechecking

    print("status: {}".format(indexer_status))
    print("last_run_status: {}".format(last_run_status))
    assert indexer_status == "running"
    assert last_run_status == "success"

    print("Indexer:")
    indexer.verify()

    # Search something
    res = index.search("London")

    print("Search status: " + str(res.status_code))
    assert res.status_code == 200
    content_string = str(res.content, 'utf-8')
    print("Results: " + content_string)
    assert content_string != ""

    # Delete all
    datasource.delete()
    index.delete()
    indexer.delete()
