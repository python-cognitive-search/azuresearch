""" ScoringProfile
"""
import json
import warnings

from azuresearch.azure_search_object import AzureSearchObject


class ScoringProfile(AzureSearchObject):
    '''
    A scoring profile for an index. See this link for more information:
    taken from
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    '''

    def __init__(self, name, text=None, functions=None, **kwargs):
        super().__init__(**kwargs)
        if functions is None:
            functions = []

        self.name = name
        self.text = text
        self.functions = functions

    def __repr__(self):
        # pylint: disable=maybe-no-member
        return "<{classname}: {name}>".format(
            classname=self.__name__, name=self.name
        )

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "text": self.text.to_dict(),
            "functions": [func.to_dict() for func in self.functions] if self.functions else None
        }

        return_dict.update(self.params)
        return_dict = self.to_camel_case_dict(return_dict)

        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")
        if 'text' in data:
            data['text'] = ScoringProfileText.load(data['text'])
        if 'functions' in data:
            data['functions'] = [ScoringProfileFunction.load(
                spf) for spf in data['functions']]

        data = cls.to_snake_case_dict(data)

        return cls(**data)


class ScoringProfileText(AzureSearchObject):
    '''
    A text value for a scoring profile. Holds the weights of different fields.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/searchservice/add-scoring-profiles-to-a-search-index
    @:param weights: a list of field name : weight value pairs
    '''

    def __init__(self, weights, **kwargs):
        super().__init__(**kwargs)
        self.weights = weights

    def to_dict(self):
        return_dict = {
            "weights": self.weights
        }

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")
        data = cls.to_snake_case_dict(data)
        return cls(**data)

# pylint: disable=too-many-instance-attributes


class ScoringProfileFunction(AzureSearchObject):
    '''
    A function to perform for scoring.
    See this link for more information:
    https://docs.microsoft.com/en-us/rest/api/
    searchservice/add-scoring-profiles-to-a-search-index#bkmk_indexref'''

    # pylint: disable=too-many-arguments
    # pylint: disable=redefined-builtin
    def __init__(self,
                 type,
                 field_name=None,
                 boost=None,
                 interpolation=None,
                 magnitude=None,
                 freshness=None,
                 distance=None,
                 tag=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.field_name = field_name
        self.boost = boost
        self.interpolation = interpolation
        self.magnitude = magnitude
        self.freshness = freshness
        self.distance = distance
        self.tag = tag

        self._validate_interpolation()

    def to_dict(self):
        return_dict = {
            "type": self.type,
            "boost": self.boost,
            "fieldName": self.field_name,
            "interpolation": self.interpolation,
            "magnitude": self.magnitude,
            "freshness": self.freshness,
            "distance": self.distance,
            "tag": self.tag
        }
        return_dict.update(self.params)
        return_dict = self.to_camel_case_dict(return_dict)

        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    def _validate_interpolation(self):
        if self.interpolation and self.interpolation not in INTERPOLATIONS:
            warnings.warn(
                "{interpolation} not in list of supported INTERPOLATIONS: {INTERPOLATIONS}".format(
                    interpolation=self.interpolation, INTERPOLATIONS=INTERPOLATIONS))


# function_types = {
#     "magnitude",
#     "freshness",
#     "distance",
#     "tag"
# }

INTERPOLATIONS = {
    "constant",
    "linear",
    "quadratic",
    "logarithmic"
}

# pylint: disable=C0301
# ``` https://docs.microsoft.com/en-us/rest/api/
# searchservice/add-scoring-profiles-to-a-search-index#bkmk_template

# "magnitude": {
#     "boostingRangeStart":  # ,
#         "boostingRangeEnd":  # ,
# "constantBoostBeyondRange": true | false(default)
# }
#
# // (- or -)
#
# "freshness": {
#     "boostingDuration": "..."(value representing timespan over which boosting occurs)
# }
#
# // (- or -)
#
# "distance": {
#     "referencePointParameter": "...", (parameter to be passed in queries to use as reference location)
#         "boostingDistance":  # (the distance in kilometers from the reference location where the boosting range ends)
# }
#
# // (- or -)
#
# "tag": {
#     "tagsParameter": "..."(parameter to be passed in queries to specify a list of tags to compare against target field)
# }
