""" AzureSearchObject
"""
import json
import re
from abc import ABC, abstractmethod

REGEX = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


class AzureSearchObject(ABC):
    """ AzureSearchObject
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: any future or optional argument to be passed to Azure Search
        """
        self.params = {}
        if kwargs:
            self.params = kwargs

    @abstractmethod
    def to_dict(self):
        """ to_dict
        """

    def to_json(self):
        """ to_json
        """
        dic = self.to_dict()
        return json.dumps(dic)

    @classmethod
    def load(cls, data):
        """ load
        """
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")

        data = cls.to_snake_case_dict(data)
        return cls(**data)

    @classmethod
    def remove_empty_values(cls, dic):
        """
        Removes all None values and empty lists from dic
        : return: new dict
        """
        dic = {k: v for k, v in dic.items() if
               (v is not None) and (not hasattr(v, '__len__') or
                                    (hasattr(v, '__len__') and len(v) > 0))}
        return dic

    @classmethod
    def to_snake_case(cls, camel_case_string):
        """ to_snake_case
        """
        return REGEX.sub(r'_\1', camel_case_string).lower()

    @classmethod
    def to_camel_case(cls, snake_case_string):
        """ to_camel_case
        """
        components = snake_case_string.split('_')
        return components[0] + ''.join(c.title() for c in components[1:])

    @classmethod
    def to_snake_case_dict(cls, dic):
        """ to_snake_case_dict
        """
        if dic:
            dic = {cls.to_snake_case(k): v for k, v in dic.items()}
        return dic

    @classmethod
    def to_camel_case_dict(cls, dic):
        """ to_camel_case_dict
        """
        if dic:
            dic = {cls.to_camel_case(k): v for k, v in dic.items()}
        return dic
