""" CustomAnalyzer
"""
import json

from .abstract_analyzer import AbstractAnalyzer


class CustomAnalyzer(AbstractAnalyzer):
    """ CustomAnalyzer
    """
    # pylint: disable=too-many-arguments

    def __init__(self,
                 name,
                 index_name=None,
                 analyzer_type="#Microsoft.Azure.Search.CustomAnalyzer",
                 char_filters=None,
                 tokenizer=None,
                 token_filters=None,
                 **kwargs):
        super().__init__(index_name=index_name, name=name,
                         analyzer_type=analyzer_type, **kwargs)

        self.tokenizer = tokenizer
        self.char_filters = char_filters
        self.token_filters = token_filters

    def to_dict(self):
        """ to_dict
        """
        return_dict = {
            "name": self.name,
            "@odata.type": self.type,
            "charFilters": self.char_filters,
            "tokenizer": self.tokenizer,
            "token_filters": self.token_filters
        }
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    # pylint: disable=arguments-differ
    @classmethod
    def load(cls, data, **kwargs):
        """ load
        """
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")
        if kwargs:
            data.update(kwargs)
        data = cls.to_snake_case_dict(data)
        return cls(**data)
