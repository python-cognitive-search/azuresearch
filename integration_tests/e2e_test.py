import time

import pytest

from azuresearch.data_source import DataSource
from azuresearch.field_mapping import FieldMapping
from azuresearch.indexers.indexer import Indexer
from azuresearch.indexes import StringField, CollectionField, Index
from azuresearch.skills import Skillset
from azuresearch.skills.predefined.cognitive_skills import EntityRecognitionSkill, KeyPhraseExtractionSkill, \
    LanguageDetectionSkill, SplitSkill, OCRSkill
from tests.test_helpers import get_json_file


@pytest.mark.integration
def test_pipeline():
    # create datasource. json holds the datasource params (name, connection string etc.)

    config = get_json_file("blob_config.json", dir='integration_tests')
    datasource = DataSource.load(config)
    datasource.delete_if_exists()
    datasource.create()

    # define fields and index
    field1 = StringField("id", key=True, sortable=True)
    field2 = StringField("content")
    field3 = StringField("languageCode", sortable=True)
    field4 = CollectionField("keyPhrases")
    field5 = CollectionField("organizations")
    field6 = StringField("translatedText")
    field7 = CollectionField("myOcrText")

    fields = [field1, field2, field3, field4, field5, field6, field7]

    index = Index("my-index", fields=fields)
    index.delete_if_exists()
    index.create()

    # Define skills
    ner_skill = EntityRecognitionSkill(categories=["Organization"])
    language_detection_skill = LanguageDetectionSkill()
    split_skill = SplitSkill(maximum_page_length=4000)
    ocr_skill = OCRSkill()
    keyphrases_skill = KeyPhraseExtractionSkill()

    skillset = Skillset(skills=[ner_skill,
                                language_detection_skill,
                                split_skill,
                                ocr_skill,
                                keyphrases_skill],
                        name="my-skillset",
                        description="skillset with one skill")
    skillset.delete_if_exists()
    skillset.create()

    field_mappings = [FieldMapping(source_field_name="metadata_storage_path",
                                   target_field_name="id",
                                   mapping_function={"name": "base64Encode"}),
                      FieldMapping("content", "content")]

    output_field_mappings = [FieldMapping("/document/organizations", "organizations"),
                             FieldMapping("/document/pages/*/keyphrases/*", "keyphrases"),
                             FieldMapping("/document/languageCode", "languageCode"),
                             FieldMapping("/document/normalized_images/*/myOcrText/", "myOcrText")]

    ## Define Indexer
    indexer = Indexer(name="my-indexer",
                      data_source_name=datasource.name,
                      target_index_name=index.name,
                      skillset_name=skillset.name,
                      field_mappings=field_mappings,
                      output_field_mappings=output_field_mappings)

    indexer.delete_if_exists()
    indexer.create()

    status = indexer.get_status()
    while status.get('status') == 'running':
        time.sleep(10)

    indexer.verify()

    ## Search something
    index.search("Microsoft")

    ## Delete all
    datasource.delete()
    index.delete()
    skillset.delete()
    indexer.delete()
