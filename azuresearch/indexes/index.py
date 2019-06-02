""" index
"""
import json

from azuresearch.base_api_call import BaseApiCall
from azuresearch.document import Documents
from .field import Field

# pylint: disable=too-many-instance-attributes


class Index(BaseApiCall):
    """ Index
    """
    results = None
    SERVICE_NAME = 'indexes'

    # pylint: disable=too-many-arguments
    def __init__(self,
                 name,
                 fields,
                 suggesters=None,
                 analyzers=None,
                 char_filters=None,
                 tokenizers=None,
                 token_filters=None,
                 scoring_profiles=None,
                 default_scoring_profile=None,
                 cors_options=None, **kwargs
                 ):
        super().__init__(Index.SERVICE_NAME, **kwargs)
        self.name = name
        self.fields = fields
        self.suggesters = suggesters
        self.analyzers = analyzers
        self.scoring_profiles = scoring_profiles
        self.tokenizers = tokenizers
        self.token_filters = token_filters
        self.char_filters = char_filters
        self.default_scoring_profile = default_scoring_profile
        self.cors_options = cors_options

        for field in self.fields:
            field.index_name = self.name

        self.documents = Documents(self)

    def __repr__(self):
        """ __repr__
        """
        return "<AzureIndex: \n" \
               "index name: {name}\n" \
               "fields: {fields}\n" \
               "scoringProfiles: {scoringProfiles}\n" \
               "corsOptions: {corsOptions}\n" \
               "suggesters: {suggesters}\n" \
               "analyzers: {analyzers}\n" \
               "tokenizers: {tokenizers}\n" \
               "tokenFilters: {tokenFilters}\n" \
               "charFilters: {charFilters}\n" \
               "defaultScoringProfile: {defaultScoringProfile}>" \
            .format(name=self.name,
                    fields="\n".join(str(field) for field in self.fields),
                    scoringProfiles=[sp for sp in self.scoring_profiles],
                    corsOptions=self.cors_options,
                    suggesters=[sg for sg in self.suggesters],
                    analyzers=[an for an in self.analyzers],
                    tokenizers=[tk for tk in self.tokenizers],
                    tokenFilters=[tkf for tkf in self.token_filters],
                    charFilters=[chf for chf in self.char_filters],
                    defaultScoringProfile=self.default_scoring_profile)

    def to_dict(self):
        """ to_dict
        """
        return_dict = {
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
            "scoringProfiles":
            [sp.to_dict()
             for sp in self.scoring_profiles] if self.scoring_profiles else None,
            "suggesters": [sg.to_dict() for sg in self.suggesters] if self.suggesters else None,
            "analyzers": [an.to_dict() for an in self.analyzers] if self.analyzers else None,
            "tokenizers": [tk.to_dict() for tk in self.tokenizers] if self.tokenizers else None,
            "tokenFilters":
            [tkf.to_dict()
             for tkf in self.token_filters] if self.token_filters else None,
            "charFilters":
            [cf.to_dict()
             for cf in self.char_filters] if self.char_filters else None,
            "corsOptions": self.cors_options,
            "defaultScoringProfile": self.default_scoring_profile
        }
        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data):
        """ load
        """
        from .suggester import Suggester
        from azuresearch.analyzers.custom_analyzer import CustomAnalyzer
        from azuresearch.indexes import ScoringProfile

        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise Exception("Failed to parse input as Dict")

        if 'suggesters' in data:
            data['suggesters'] = [Suggester.load(
                sg) for sg in data.get("suggesters")]

        if 'analyzers' in data:
            data['analyzers'] = [CustomAnalyzer.load(
                sg, index_name=data.get('name')) for sg in data.get('analyzers')]

        if 'scoringProfiles' in data:
            data['scoring_profiles'] = [ScoringProfile.load(
                sp) for sp in data['scoringProfiles']]

        if 'fields' in data:
            data['fields'] = [Field.load(fi) for fi in data['fields']]

        data = cls.to_snake_case_dict(data)

        return cls(**data)

    def verify(self):
        """ verify
        """
        return self.get()

    def search(self, query):
        """ search
        """
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "all"
        }
        self.results = self.endpoint.post(
            query, endpoint=self.name + "/docs/search")
        return self.results

    def statistics(self):
        """ statistics
        """
        response = self.endpoint.get(
            endpoint=self.name + "/stats", needs_admin=True)
        if response.status_code == 200:
            recent_stats = response.json()
            return recent_stats
        return response

    def count(self):
        """ count
        """
        # https://docs.microsoft.com/en-us/rest/api/searchservice/count-documents
        response = self.endpoint.get(
            endpoint=self.name + "/docs/$count", needs_admin=True)
        if response.status_code == 200:
            response.encoding = "utf-8-sig"
            recent_count = int(response.text)
            return recent_count
        return response
