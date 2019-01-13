import json

from azuresearch.base_api_call import BaseApiCall
from azuresearch.document import Documents
from azuresearch.service import Endpoint
from .field import Field

SERVICE_NAME = 'indexes'


class Index(BaseApiCall):
    results = None

    def __init__(self,
                 name,
                 fields=None,
                 suggesters=None,
                 analyzers=None,
                 char_filters=None,
                 tokenizers=None,
                 token_filters=None,
                 scoring_profiles=None,
                 default_scoring_profile=None,
                 cors_options=None, **kwargs
                 ):
        super(Index, self).__init__(SERVICE_NAME)
        if fields is None:
            fields = []
        if analyzers is None:
            analyzers = []
        if suggesters is None:
            suggesters = []
        if scoring_profiles is None:
            scoring_profiles = []
        if tokenizers is None:
            tokenizers = []
        if token_filters is None:
            token_filters = []
        if char_filters is None:
            char_filters = []

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
        self.params = {}
        if kwargs:
            self.params.update(kwargs)

        for f in self.fields:
            f.index_name = self.name

        self.documents = Documents(self)

    def __repr__(self):
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
        return_dict = {
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
            "scoringProfiles": [sp.to_dict() for sp in self.scoring_profiles],
            "corsOptions": self.cors_options,
            "suggesters": [sg.to_dict() for sg in self.suggesters],
            "analyzers": [an.to_dict() for an in self.analyzers],
            "tokenizers": [tk.to_dict() for tk in self.tokenizers],
            "tokenFilters": [tkf.to_dict() for tkf in self.token_filters],
            "charFilters": [cf.to_dict() for cf in self.char_filters],
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
        from .suggester import Suggester
        from azuresearch.analyzers.custom_analyzer import CustomAnalyzer
        from azuresearch.indexes import ScoringProfile

        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")

        if 'suggesters' in data:
            data['suggesters'] = [Suggester.load(sg) for sg in data.get("suggesters")]

        if 'analyzers' in data:
            data['analyzers'] = [CustomAnalyzer.load(sg,index_name=data.get('name')) for sg in data.get('analyzers')]

        if 'scoringProfiles' in data:
            data['scoring_profiles'] = [ScoringProfile.load(sp) for sp in data['scoringProfiles']]

        if 'fields' in data:
            data['fields'] = [Field.load(fi) for fi in data['fields']]

        data = cls.to_snake_case_dict(data)

        return cls(**data)

    def create(self):
        return self.endpoint.post(self.to_dict(), needs_admin=True)

    def update(self):
        self.delete()
        return self.create()

    def get(self):
        return self.endpoint.get(endpoint=self.name, needs_admin=True)

    def delete(self):
        return self.endpoint.delete(endpoint=self.name, needs_admin=True)

    def verify(self):
        return self.get()

    @classmethod
    def list(cls):
        return Endpoint(SERVICE_NAME).get(needs_admin=True)

    def search(self, query):
        query = {
            "search": query,
            "queryType": "full",
            "searchMode": "all"
        }
        self.results = self.endpoint.post(query, endpoint=self.name + "/docs/search")
        return self.results

    def statistics(self):
        response = self.endpoint.get(endpoint=self.name + "/stats", needs_admin=True)
        if response.status_code == 200:
            self.recent_stats = response.json()
            return self.recent_stats
        else:
            return response

    def count(self):
        # https://docs.microsoft.com/en-us/rest/api/searchservice/count-documents
        response = self.endpoint.get(endpoint=self.name + "/docs/$count", needs_admin=True)
        if response.status_code == 200:
            response.encoding = "utf-8-sig"
            self.recent_count = int(response.text)
            return self.recent_count
        else:
            return response
