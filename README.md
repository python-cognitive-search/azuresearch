[![Build Status](https://dev.azure.com/csedevil/Azure%20search%20pyhton/_apis/build/status/python-cognitive-search.azuresearch?branchName=master)](https://dev.azure.com/csedevil/Azure%20search%20pyhton/_build/latest?definitionId=68?branchName=master)
![Issues](https://img.shields.io/github/issues/python-cognitive-search/azuresearch.svg?style=flat)
![Coverage](https://img.shields.io/azure-devops/coverage/csedevil/Azure%20search%20pyhton/68.svg?style=flat)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

---
# Cognitive Search - Python package 

Create Indexes, indexers, suggesters, analyzers, scoring profiles, custom and predefined skills via Python.
Upload documents or manage data sources for Azure Search.
Create a data pipeline from source, through cognitive skills (either predefined or custom), into Azure Search 


For this to work you need the following environment variables set:

    AZURE_SEARCH_API_KEY={a regular search api key}
    AZURE_SEARCH_ADMIN_API_KEY={a search admin api key}
    AZURE_SEARCH_URL=https://{your search service name}.search.windows.net

Features:
1. Define fields and indexes through Python
2. Deine skills and skillsets: Predefined Cognitive Search skills and custom skills (WebAPI skills)
3. Define analyzers (custom analyzers and predefined analyzers)
4. Define scoring profiles, suggesters
5. Upload documents to Azure Search 
6. Manage data sources



originally forked from https://github.com/python-azure-search/python-azure-search


Example usage (WIP):

```python

    # Create a new data source:
    datasource = DataSource(name="myblob", connection_string="my_connection_string", container_name="mycontainer")
    
    # Delete the data source if exists previously:
    datasource.delete_if_exists()
    datasource.create()

    # Define fields and index:
    id_field = StringField("id", key=True, sortable=True)
    content_field = StringField("content")
    language_code_field = StringField("languageCode", sortable=True)
    key_phrases_field = CollectionField("keyPhrases")
    organizations_field = CollectionField("organizations")
    translated_text_field = StringField("translatedText")

    fields = [id_field, content_field, language_code_field, key_phrases_field, organizations_field,
              translated_text_field]

    # Create index:
    index = Index("my-index", fields=fields)
    index.delete_if_exists()
    index.create()

    # Create skillset: 
    # We want to have a pipeline with NER detecting organizations, and keyphrases extracted.
    # the Keyphrase skill requires the text to be splitted, so we use the Split skill. It also requires the language, 
    # so we use the Language Detection skill.
    # In addition, we want organizations and key phrases to be stored as fields in the index.
    
    # Our pipeline's dependency list:
    # 1: ner_skill
    # 1: language_detection_skill
    # 1: split_skill
    # 2: (splitskill , language code) -> keyphrases_skill
    
    # Define skills, Including the matching field mapping:
    ner_skill = EntityRecognitionSkill(categories=["Organization"])
    language_detection_skill = LanguageDetectionSkill()
    split_skill = SplitSkill(maximum_page_length=4000)
    keyphrases_skill = KeyPhraseExtractionSkill()

    # map skills output to fields (aka FieldOutputMapping)
    keyphrases_skill.key_phrases.map_to(key_phrases_field)
    ner_skill.organization.map_to(organizations_field)
    language_detection_skill.language_code.map_to(language_code_field)

    # Connect one skill to previous skills outputs:
    keyphrases_skill.set_inputs(text=split_skill.text_items,
                                language_code=language_detection_skill.language_code)


    # Create the skillset with our previously defined fields:
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

    # Indexer is now indexing our data per our defined pipeline

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

    # Search:
    res = index.search("Microsoft")

    print("Search status: " + str(res.status_code))
    content_string = str(res.content, 'utf-8')
    print("Results: " + content_string)

```
