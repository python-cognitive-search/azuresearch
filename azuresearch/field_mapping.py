""" FieldMapping
"""
import json

from azuresearch.azure_search_object import AzureSearchObject


class FieldMapping(AzureSearchObject):
    """ FieldMapping
    """

    def __init__(self, source_field_name, target_field_name=None, mapping_function=None, **kwargs):
        """
        :param source_field_name: which represents a field in your data source.
               This property is required.
        :param target_field_name: which represents a field in your search index.
               If omitted, the same name as in the data source is used.
        :param mapping_function:
               Transforms your data using one of several predefined functions.
               See here for more info:
               https://docs.microsoft.com/en-us/azure/search/search-indexer-field-mappings#mappingFunctions
        """
        super().__init__(**kwargs)
        self.source_field_name = source_field_name
        self.target_field_name = target_field_name
        self.mapping_function = mapping_function


    def __repr__(self):
        """

        :return:
        """
        return json.dumps(self.to_dict())

    def to_dict(self):
        """ to_dict
        """
        return_dict = {"source_field_name": self.source_field_name,
                       "target_field_name": self.target_field_name,
                       "mapping_function": self.mapping_function}

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict
