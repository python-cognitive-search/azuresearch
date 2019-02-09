import os
import time

import pytest

from azuresearch.data_source import DataSource
from azuresearch.field_mapping import FieldMapping
from azuresearch.indexers import IndexerParameters
from azuresearch.indexers.indexer import Indexer
from azuresearch.indexes import StringField, CollectionField, Index
from azuresearch.skills import Skillset
from azuresearch.skills.predefined.cognitive_skills import (
    EntityRecognitionSkill,
    KeyPhraseExtractionSkill,
    LanguageDetectionSkill,
    SplitSkill,
)
from tests.test_helpers import get_json_file

path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.integration
def test_pipeline():
    # create datasource. json holds the datasource params (name, connection string etc.)

    config = get_json_file("blob_config.json", path=path, dir=None)
    datasource = DataSource.load(config)
    # delete the data source to to support quick iterations
    datasource.delete_if_exists()
    datasource.create()

    # define fields and index
    field1 = StringField("id", key=True, sortable=True)
    field2 = StringField("content")
    field3 = StringField("languageCode", sortable=True)
    field4 = CollectionField("keyPhrases")
    field5 = CollectionField("organizations")
    field6 = StringField("translatedText")

    fields = [field1, field2, field3, field4, field5, field6]

    index = Index("my-index", fields=fields)
    index.delete_if_exists()
    index.create()

    # Define skills, Including the matching field mapping
    ner_skill = EntityRecognitionSkill(
        categories=["Organization"],
        fields_mapping=[{"name": EntityRecognitionSkill.SupportedTypes.ORGANIZATION, "field": field5}])
    language_detection_skill = LanguageDetectionSkill(
        fields_mapping=[{"name": LanguageDetectionSkill.SupportedTypes.LANGUAGE_CODE, "field": field3}])
    split_skill = SplitSkill(maximum_page_length=4000)
    keyphrases_skill = KeyPhraseExtractionSkill(
        fields_mapping=[{"name": KeyPhraseExtractionSkill.SupportedTypes.TEXT, "field": field4}])

    # dependency list:
    # 1: ner_skill
    # 1: language_detection_skill
    # 1: split_skill
    # 2: splitskill , language code-> keyphrases_skill
    # keyphrases_skill.add_source(split_skill)
    # keyphrases_skill.add_source(language_detection_skill)

    skillset = Skillset(
        skills=[
            ner_skill,
            language_detection_skill,
            split_skill,
            keyphrases_skill,
        ],
        name="my-skillset",
        description="skillset with one skill",
    )
    skillset.delete_if_exists()
    skillset.create()

    # Define Indexer
    config = IndexerParameters()
    indexer = Indexer(
        name="my-indexer",
        data_source_name=datasource.name,
        target_index_name=index.name,
        skillset_name=skillset.name,
        output_field_mappings=skillset.get_output_field_mappings()
    )

    indexer.delete_if_exists()
    indexer.create()

    indexer_status = ""
    last_run_status = None
    while indexer_status != "error" and (last_run_status is None or last_run_status == "inProgress"):
        status = indexer.get_status()
        indexer_status = status.get("status")
        last_run_status = status.get("lastResult")
        if last_run_status is not None:
            last_run_status = last_run_status.get("status")
            print("last run status: " + last_run_status)

        print("indexer status is: " + indexer_status)
        time.sleep(3)  # wait for 3 seconds until rechecking

    assert indexer_status == "running"
    assert last_run_status == "success"

    indexer.verify()

    # Search something
    res = index.search("Microsoft")

    print("Search status: " + str(res.status_code))
    assert res.status_code == 200
    content_string = str(res.content, 'utf-8')
    print("Results: " + content_string)
    assert content_string != ""

    # Delete all
    datasource.delete()
    index.delete()
    skillset.delete()
    indexer.delete()
