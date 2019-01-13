import json
import re
from abc import ABC, abstractmethod

regex = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


class AzureSearchObject(ABC):

    def __init__(self,**kwargs):
        """
        :param kwargs: any future or optional argument to be passed to Azure Search
        """
        self.params = {}
        if kwargs:
            self.params = kwargs

    @abstractmethod
    def to_dict(self):
        pass

    def toJSON(self):
        dict = self.to_dict()
        return json.dumps(dict)

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        data = cls.to_snake_case_dict(data)
        return cls(**data)

    @classmethod
    def remove_empty_values(cls, dict):
        """
        Removes all None values and empty lists from dict
        :return: new dict
        """
        dict = {k: v for k, v in dict.items() if
                (v is not None) and (not hasattr(v, '__len__') or (hasattr(v, '__len__') and len(v) > 0))}
        return dict

    @classmethod
    def to_snake_case(cls, camel_case_string):
        return regex.sub(r'_\1', camel_case_string).lower()

    @classmethod
    def to_camel_case(cls,snake_case_string):
        components = snake_case_string.split('_')
        return components[0] + ''.join(c.title() for c in components[1:])

    @classmethod
    def to_snake_case_dict(cls, dict):
        if dict:
            dict = {cls.to_snake_case(k): v for k, v in dict.items()}
        return dict

    @classmethod
    def to_camel_case_dict(cls, dict):
        if dict:
            dict = {cls.to_camel_case(k): v for k, v in dict.items() }
        return dict
