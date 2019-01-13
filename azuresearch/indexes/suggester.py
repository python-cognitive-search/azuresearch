import json

from azuresearch.base_api_call import BaseApiCall


class Suggester(BaseApiCall):

    def __init__(self, name, source_fields, search_mode="analyzingInfixMatching",**kwargs):
        super().__init__("indexes",**kwargs)
        self.name = name
        self.source_fields = source_fields
        self.search_mode = search_mode

    def __repr__(self):
        return "<Suggester: {name}>".format(
            name=self.name
        )

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "sourceFields": [field for field in self.source_fields],
            "searchMode": self.search_mode
        }

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    def suggest(self, query, extra=None):
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "analyzingInfixMatching"
        }
        self.results = self.endpoint.post(query, endpoint=self.name + "/docs/suggest")
        return self.results
