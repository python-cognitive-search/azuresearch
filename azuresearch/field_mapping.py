import json

from azuresearch.azure_search_object import AzureSearchObject


class FieldMapping(AzureSearchObject):

    def __init__(self, source_field_name, target_field_name=None, mapping_function=None):
        """
        :param source_field_name: which represents a field in your data source. This property is required.
        :param target_field_name: which represents a field in your search index. If omitted, the same name as in the data source is used.
        :param mapping_function: Transforms your data using one of several predefined functions. See here for more info: https://docs.microsoft.com/en-us/azure/search/search-indexer-field-mappings#mappingFunctions
        """
        self.source_field_name = source_field_name
        self.target_field_name = target_field_name
        self.mapping_function = mapping_function

    def to_dict(self):
        dict = {"sourceFieldName": self.source_field_name,
                "targetFieldName": self.target_field_name,
                "mappingFunction": self.mapping_function}

        dict = FieldMapping.remove_empty_values(dict)
        return dict

    @classmethod
    def load(cls, data):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load class")

            if 'sourceFieldName' not in data:
                data['sourceFieldName'] = None
            if 'targetFieldName' not in data:
                data['targetFieldName'] = None
            if 'mappingFunction' not in data:
                data['mappingFunction'] = None
            return cls(source_field_name=data['sourceFieldName'], target_field_name=data['targetFieldName'],
                       mapping_function=data['mappingFunction'])
        else:
            raise Exception("data is Null")
