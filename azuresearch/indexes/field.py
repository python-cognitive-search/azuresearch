import json

from azuresearch.azure_search_object import AzureSearchObject


class Field(AzureSearchObject):
    """
    :param name: name_of_field,
    :param type: Edm.String | Collection(Edm.String) | Edm.Int32 | Edm.Int64 | Edm.Double | Edm.Boolean | Edm.DateTimeOffset | Edm.GeographyPoint,
    :param searchable: true (default where applicable) | false (only Edm.String and Collection(Edm.String) fields can be searchable),
    :param filterable: true (default) | false,
    :param retrievable: true (default) | false,
    :param sortable: true (default where applicable) | false (Collection(Edm.String) fields cannot be sortable),
    :param facetable: true (default where applicable) | false (Edm.GeographyPoint fields cannot be facetable),
    :param key: true | false (default, only Edm.String fields can be keys),
    :param index_analyzer: name of the indexing analyzer (only if 'searchAnalyzer' is set and 'analyzer' is not set)
    :param search_analyzer: name of the search analyzer, (only if 'indexAnalyzer' is set and 'analyzer' is not set)
    :param analyzer: Sets the name of the language analyzer to use for the field.
    For the allowed set of values see Language support (https://docs.microsoft.com/en-us/rest/api/searchservice/language-support).
    This option can be used only with searchable fields and it can't be set together with either search_analyzer or index_analyzer.
    Once the analyzer is chosen, it cannot be changed for the field.
    :param synonym_maps: List of synonym map to use for this index
    """
    python_type = None

    def __init__(self,
                 name,
                 type=None,
                 index_name=None,
                 searchable=False,
                 filterable=True,
                 retrievable=True,
                 sortable=True,
                 facetable=True,
                 key=False,
                 index_analyzer=None,
                 search_analyzer=None,
                 analyzer=None,
                 synonym_maps=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.index_name = index_name
        self.searchable = searchable
        self.filterable = filterable
        self.retrievable = retrievable
        self.sortable = sortable
        self.facetable = facetable
        self.key = key
        self.index_analyzer = index_analyzer
        self.search_analyzer = search_analyzer
        self.analyzer = analyzer
        self.synonym_maps = synonym_maps

        if type is not None:
            self._field_type = type

        self._validate_type()
        self._validate_name()

    def __repr__(self):
        return "Index.Field : {index}.{name}".format(
            index=self.index_name, name=self.name
        )

    @property
    def field_type(self):
        if hasattr(self, '_field_type') and self._field_type is not None:
            return self._field_type
        else:
            return "Edm.{}".format(self.__class__.__name__.replace('Field', ""))

    def _validate_type(self):
        if self.field_type not in types.keys():
            raise ValueError("Azure Search only supports these types: {types}".format(types=types.keys()))

    def _validate_name(self):
        if self.name is None or self.name == "":
            raise ValueError("Field must have a name")

    def to_dict(self):
        return_dict = {
            "name": self.name,
            "type": self.field_type,
            "searchable": self.searchable,
            "filterable": self.filterable,
            "sortable": self.sortable,
            "facetable": self.facetable,
            "key": self.key,
            "retrievable": self.retrievable,
            "analyzer": self.analyzer,
            "searchAnalyzer": self.search_analyzer,
            "indexAnalyzer": self.index_analyzer,
            "synonymMaps": self.synonym_maps
        }

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict

    @classmethod
    def load(cls, data, **kwargs):
        if data:
            if type(data) is str:
                data = json.loads(data)
            if type(data) is not dict:
                raise Exception("Failed to load JSON file with field data")
            field_type = types[data.pop('type')]

            kwargs.update(data)
            kwargs = cls.to_snake_case_dict(kwargs)
            return field_type(**kwargs)
        else:
            raise Exception("data is None")


class StringField(Field):
    python_type = str

    def __init__(self, name, searchable=True, key=False, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.key = key
        self.searchable = searchable


class CollectionField(Field):
    _field_type = "Collection(Edm.String)"

    def __init__(self, name, searchable=True, key=False, *args, **kwargs):
        kwargs['sortable'] = False  # Collections cannot be sortable
        super().__init__(name, "Collection(Edm.String)", *args, **kwargs)
        self.searchable = searchable


class Int32Field(Field):
    python_type = int


class Int64Field(Field):
    python_type = int


class DoubleField(Field):
    python_type = float


class BooleanField(Field):
    python_type = bool


class DateTimeOffsetField(Field):
    python_type = None


class GeographyPointField(Field):
    def __init__(self, name, facetable=False, *args, **kwargs):
        kwargs['facetable'] = False  # Edm.GeographyPoint fields cannot be facetable
        super().__init__(name, *args, **kwargs)


types = {
    "Edm.String": StringField,
    "Collection(Edm.String)": CollectionField,
    "Edm.Int32": Int32Field,
    "Edm.Int64": Int64Field,
    "Edm.Double": DoubleField,
    "Edm.Boolean": BooleanField,
    "Edm.DateTimeOffset": DateTimeOffsetField,
    "Edm.GeographyPoint": GeographyPointField
}
