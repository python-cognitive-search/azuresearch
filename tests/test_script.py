import pytest

from azuresearch.data_source import DataSource
from azuresearch.indexer import Indexer
from azuresearch.indexes import StringField, CollectionField, Index
from azuresearch.skills import SkillInput, Skillset
from azuresearch.skills.predefined.cognitive_skills import EntityRecognitionSkill, KeyPhraseExtractionSkill
from tests.test_helpers import get_json_file

@pytest.mark.integration
def test_pipeline():

    #create datasource. json holds the datasource params (name, connection string etc.)

    config = get_json_file("blob_config.json",dir='integration_tests')
    datasource = DataSource.load(config)
    datasource.delete_if_exists()
    datasource.create()

    # define fields and index
    field1 = StringField("id",key=True)
    field2 = CollectionField("keyPhrases")
    field3 = StringField("content")


    index = Index("my-index",fields = [field1,field2,field3])
    index.delete_if_exists()
    index.create()

    # Define skills
    ner_skill = KeyPhraseExtractionSkill()
    skillset = Skillset(skills=[ner_skill],name="my-skillset",description="skillset with one skill")
    skillset.delete_if_exists()
    skillset.create()


    ## Define Indexer
    indexer = Indexer(name="my-indexer",
                      data_source_name=datasource.name,
                      target_index_name=index.name,
                      skillset_name=skillset.name
                      )
    indexer.delete_if_exists()
    indexer.create()

    ## Search something
    index.search("Microsoft")


    ## Delete all
    datasource.delete()
    index.delete()
    skillset.delete()
    indexer.delete()
