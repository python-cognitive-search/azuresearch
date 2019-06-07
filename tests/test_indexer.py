from azuresearch.field_mapping import FieldMapping
from azuresearch.indexers import Indexer


def test_indexer_to_dict():
    fm = FieldMapping("content1","content1")
    indexer = Indexer(name='my-indexer',
                      data_source_name='my-data',
                      target_index_name='my-index',
                      skillset_name=None,
                      field_mappings=[fm])

    assert indexer.to_dict()['name'] == 'my-indexer'
    assert indexer.to_dict()['fieldMappings'][0] == fm.to_dict()
