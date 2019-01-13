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
