# Cognitive Search - Python package [![Build Status](https://dev.azure.com/csedevil/Azure%20search%20pyhton/_apis/build/status/python-cognitive-search.azuresearch?branchName=master)](https://dev.azure.com/csedevil/Azure%20search%20pyhton/_build/latest?definitionId=68?branchName=master)
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
    #create datasource. json holds the datasource params (name, connection string etc.)

    datasource = DataSource.load(name="datasource",connection_string="xxx",container_name="cont")
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
    keyph_skill = KeyPhraseExtractionSkill()
    skillset = Skillset(skills=[keyph_skill],name="my-skillset",description="skillset with one skill")
    skillset.delete_if_exists()
    skillset.create()


    ## Define Indexer
    indexer = Indexer(name="my-indexer", data_source_name=datasource.name,
                      target_index_name=index.name, skillset_name=skillset.name)
    indexer.delete_if_exists()
    indexer.create()

    status = indexer.get_status()
    while status.get('status') == 'running':
        print(status.get("status"))
        time.sleep(10) # wait for x seconds until rechecking
    
    indexer.verify()
    
    ## Search something
    res = index.search("Microsoft")
    print(res)

    ## Delete all
    datasource.delete()
    index.delete()
    skillset.delete()
    indexer.delete()

```
