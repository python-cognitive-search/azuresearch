from azuresearch.service import Endpoint
from .abstract_analyzer import AbstractAnalyzer


class PredefinedAnalyzer(AbstractAnalyzer):
    __name__ = 'PredefinedAnalyzer'
    endpoint = Endpoint("indexes")

    def __init__(self, index_name, name, type, options=None,**kwargs):
        super(PredefinedAnalyzer, self).__init__(index_name, name, type,**kwargs)
        self.options = options

    def to_dict(self):
        return_dict= {
            "name": self.name,
            "@odata.type": self.type,
            "searchMode": self.search_mode,
            "options": self.options
        }

        # add additional user generated params
        return_dict.update(self.params)
        # make all params camelCase (to be sent correctly to Azure Search
        return_dict = self.to_camel_case_dict(return_dict)

        # Remove None values
        return_dict = self.remove_empty_values(return_dict)
        return return_dict


predefined_analyzers = {
    "keyword": None,
    "pattern": "#Microsoft.Azure.Search.PatternAnalyzer",
    "simple": None,
    "standard": "#Microsoft.Azure.Search.StandardAnalyzer",
    "standardasciifolding.lucene": None,
    "stop": "#Microsoft.Azure.Search.StopAnalyzer",
    "whitespace": None
}

char_filters = {
    "html_strip", None,
    "mapping", "#Microsoft.Azure.Search.MappingCharFilter",
    "pattern_replace", "#Microsoft.Azure.Search.PatternReplaceCharFilter"
}

tokenizers = {
    "classic": "#Microsoft.Azure.Search.ClassicTokenizer",
    "edgeNGram": "#Microsoft.Azure.Search.EdgeNGramTokenizer",
    "keyword_v2": "#Microsoft.Azure.Search.KeywordTokenizerV2",
    "letter": None,
    "lowercase": None,
    "microsoft_language_tokenizer": "#Microsoft.Azure.Search.MicrosoftLanguageTokenizer",
    "microsoft_language_stemming_tokenizer": "#Microsoft.Azure.Search.MicrosoftLanguageStemmingTokenizer",
    "ngram": "#Microsoft.Azure.Search.NGramTokenizer",
    "path_hierarchy_v2": "#Microsoft.Azure.Search.PathHierarchyTokenizerV2",
    "pattern": "#Microsoft.Azure.Search.PatternTokenizer",
    "standard_v2": "#Microsoft.Azure.Search.StandardTokenizerV2",
    "uax_url_email": "#Microsoft.Azure.Search.UaxUrlEmailTokenizer",
    "whitespace": None
}

token_filters = {
    "arabic_normalization": None,
    "apostrophe": None,
    "asciifolding": "#Microsoft.Azure.Search.AsciiFoldingTokenFilter",
    "cjk_bigram": "#Microsoft.Azure.Search.CjkBigramTokenFilter",
    "cjk_width": None,
    "classic": None,
    "common_grams": "#Microsoft.Azure.Search.CommonGramTokenFilter",
    "dictionary_decompounder": "#Microsoft.Azure.Search.DictionaryDecompounderTokenFilter",
    "edgeNGram_v2": "#Microsoft.Azure.Search.EdgeNGramTokenFilterV2",
    "elision": "#Microsoft.Azure.Search.ElisionTokenFilter",
    "german_normalization": None,
    "hindi_normalization": None,
    "indic_normalization": "#Microsoft.Azure.Search.IndicNormalizationTokenFilter",
    "keep": "#Microsoft.Azure.Search.KeepTokenFilter",
    "keyword_marker": "#Microsoft.Azure.Search.KeywordMarkerTokenFilter",
    "keyword_repeat": None,
    "kstem": None,
    "length": "#Microsoft.Azure.Search.LengthTokenFilter",
    "limit": "#Microsoft.Azure.Search.Microsoft.Azure.Search.LimitTokenFilter",
    "lowercase": None,
    "nGram_v2": "#Microsoft.Azure.Search.NGramTokenFilterV2",
    "pattern_capture": "#Microsoft.Azure.Search.PatternCaptureTokenFilter",
    "pattern_replace": "#Microsoft.Azure.Search.PatternReplaceTokenFilter",
    "persian_normalization": None,
    "phonetic": "#Microsoft.Azure.Search.PhoneticTokenFilter",
    "porter_stem": None,
    "reverse": None,
    "scandinavian_normalization": None,
    "scandinavian_folding": None,
    "shingle": "#Microsoft.Azure.Search.ShingleTokenFilter",
    "snowball": "#Microsoft.Azure.Search.SnowballTokenFilter",
    "sorani_normalization": "#Microsoft.Azure.Search.SoraniNormalizationTokenFilter",
    "stemmer": "#Microsoft.Azure.Search.StemmerTokenFilter",
    "stemmer_override": "#Microsoft.Azure.Search.StemmerOverrideTokenFilter",
    "stopwords": "#Microsoft.Azure.Search.StopwordsTokenFilter",
    "synonym": "#Microsoft.Azure.Search.SynonymTokenFilter",
    "trim": None,
    "truncate": "#Microsoft.Azure.Search.TruncateTokenFilter",
    "unique": "#Microsoft.Azure.Search.UniqueTokenFilter",
    "uppercase": None,
    "word_delimiter": "#Microsoft.Azure.Search.WordDelimiterTokenFilter"
}
